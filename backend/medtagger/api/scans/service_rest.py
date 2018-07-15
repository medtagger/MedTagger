"""Module responsible for definition of Scans service available via HTTP REST API."""
import json
from typing import Any

from flask import request
from flask_restplus import Resource
from jsonschema import validate, ValidationError, Draft4Validator
from jsonschema.exceptions import best_match

from medtagger.types import ScanID
from medtagger.api import api
from medtagger.api.exceptions import InvalidArgumentsException
from medtagger.api.scans import business, serializers
from medtagger.api.security import login_required, role_required
from medtagger.api.scans.serializers import elements_schema

scans_ns = api.namespace('scans', 'Methods related with scans')


@scans_ns.route('/')
class Scans(Resource):
    """Endpoint that can create new scan."""

    @staticmethod
    @login_required
    @role_required('doctor', 'admin')
    @scans_ns.expect(serializers.in__new_scan)
    @scans_ns.marshal_with(serializers.out__new_scan)
    @scans_ns.doc(security='token')
    @scans_ns.doc(description='Creates empty scan.')
    @scans_ns.doc(responses={201: 'Success'})
    def post() -> Any:
        """Create empty scan."""
        payload = request.json
        category_key = payload['category']
        number_of_slices = payload['number_of_slices']
        if not business.scan_category_is_valid(category_key):
            raise InvalidArgumentsException('Category "{}" is not available.'.format(category_key))

        scan = business.create_empty_scan(category_key, number_of_slices)
        return scan, 201


@scans_ns.route('/categories')
class ScanCategories(Resource):
    """Endpoint that manages categories."""

    @staticmethod
    @login_required
    @scans_ns.marshal_with(serializers.out__scan_category)
    @scans_ns.doc(security='token')
    @scans_ns.doc(description='Returns all available scan categories.')
    @scans_ns.doc(responses={200: 'Success'})
    def get() -> Any:
        """Return all available scan categories."""
        return business.get_available_scan_categories()

    @staticmethod
    @login_required
    @role_required('doctor', 'admin')
    @scans_ns.expect(serializers.in__scan_category)
    @scans_ns.marshal_with(serializers.in__scan_category)
    @scans_ns.doc(security='token')
    @scans_ns.doc(description='Create new Scan Category.')
    @scans_ns.doc(responses={201: 'Success'})
    def post() -> Any:
        """Create Scan Category."""
        payload = request.json
        key = payload['key']
        name = payload['name']
        image_path = payload['image_path']

        return business.create_scan_category(key, name, image_path), 201


@scans_ns.route('/tasks')
class Tasks(Resource):
    """Endpoint that manages tasks."""

    @staticmethod
    @login_required
    @scans_ns.marshal_with(serializers.out__task)
    @scans_ns.doc(security='token')
    @scans_ns.doc(description='Return all available tasks.')
    @scans_ns.doc(responses={200: 'Success'})
    def get() -> Any:
        """Return all available tasks."""
        return business.get_tasks()

    @staticmethod
    @login_required
    @role_required('doctor', 'admin')
    @scans_ns.expect(serializers.in__task)
    @scans_ns.marshal_with(serializers.in__scan_category)
    @scans_ns.doc(security='token')
    @scans_ns.doc(description='Create new Scan Category.')
    @scans_ns.doc(responses={201: 'Success'})
    def post() -> Any:
        """Create Scan Category."""
        payload = request.json
        key = payload['key']
        name = payload['name']
        image_path = payload['image_path']

        return business.create_task(key, name, image_path), 201


@scans_ns.route('/random')
class Random(Resource):
    """Endpoint that returns random scan for labeling from specified task."""

    @staticmethod
    @login_required
    @scans_ns.expect(serializers.args__random_scan)
    @scans_ns.marshal_with(serializers.out__scan)
    @scans_ns.doc(security='token')
    @scans_ns.doc(description='Returns random scan from task.')
    @scans_ns.doc(responses={200: 'Success', 400: 'Invalid arguments', 404: 'No Scans available'})
    def get() -> Any:
        """Return random Scan."""
        args = serializers.args__random_scan.parse_args(request)
        task_key = args.task
        if not business.task_key_is_valid(task_key):
            raise InvalidArgumentsException('Task "{}" is not available.'.format(task_key))
        return business.get_random_scan(task_key)


@scans_ns.route('/<string:scan_id>/label')
@scans_ns.param('scan_id', 'Scan identifier')
class Label(Resource):
    """Endpoint that stores label for given scan."""

    @staticmethod
    @login_required
    @scans_ns.expect(serializers.in__label)
    @scans_ns.marshal_with(serializers.out__label)
    @scans_ns.doc(security='token')
    @scans_ns.doc(description='Stores label and assigns it to given scan.')
    @scans_ns.doc(responses={201: 'Successfully saved', 400: 'Invalid arguments', 404: 'Could not find scan or tag'})
    def post(scan_id: ScanID) -> Any:
        """Add new Label for given scan.

        This endpoint needs a multipart/form-data content where there is one mandatory section called "label".
        Such section will contain a JSON payload with representation of a Label. If such Label needs additional
        information like images (binary mask), please attach them as a separate part.

        Here is an example CURL command that sends Label with Brush Element:

            $> curl -v
                    -H "Content-Type:multipart/form-data"
                    -H "Authorization: Bearer MEDTAGGER_API_TOKEN"
                    -F "SLICE_1=@"/Users/jakubpowierza/Desktop/test.png""
                    -F "label={"elements": [{"width": 1, "height": 1, "image_key": "SLICE_1",
                               "slice_index": 1, "tag": "LEFT_KIDNEY", "tool": "BRUSH"}],
                               "labeling_time": 0.1};type=application/json"
                     http://localhost:51000/api/v1/scans/c5102707-cb36-4869-8041-f00421c03fa1/label
        """
        files = {name: file_data.read() for name, file_data in request.files.items()}
        label = json.loads(request.form['label'])
        elements = label['elements']
        try:
            validate(elements, elements_schema)
        except ValidationError:
            validator = Draft4Validator(elements_schema)
            errors = validator.iter_errors(elements)
            best_error = best_match(errors)
            raise InvalidArgumentsException(best_error.message)

        business.validate_label_payload(elements, files)

        labeling_time = label['labeling_time']
        label = business.add_label(scan_id, elements, files, labeling_time)
        return label, 201


@scans_ns.route('/<string:scan_id>')
@scans_ns.param('scan_id', 'Scan identifier')
class Scan(Resource):
    """Endpoint that returns scan for the given scan id."""

    @staticmethod
    @login_required
    @scans_ns.marshal_with(serializers.out__scan)
    @scans_ns.doc(security='token')
    @scans_ns.doc(description='Returns scan with given scan_id.')
    @scans_ns.doc(responses={200: 'Success', 404: 'Could not find scan'})
    def get(scan_id: ScanID) -> Any:
        """Return scan for the given scan_id."""
        return business.get_scan(scan_id)


@scans_ns.route('/<string:scan_id>/skip')
@scans_ns.param('scan_id', 'Scan identifier')
class SkipScan(Resource):
    """Endpoint that allows for skipping given Scan."""

    @staticmethod
    @login_required
    @scans_ns.doc(security='token')
    @scans_ns.doc(description='Increases skip count of a scan with given scan_id.')
    @scans_ns.doc(responses={200: 'Success', 404: 'Could not find scan'})
    def post(scan_id: ScanID) -> Any:
        """Increases skip count of a scan with given scan_id."""
        if not business.skip_scan(scan_id):
            return '', 404
        return '', 200


@scans_ns.route('/<string:scan_id>/slices')
@scans_ns.param('scan_id', 'Scan identifier')
class ScanSlices(Resource):
    """Endpoint that allows for uploading Slices to given Scan."""

    @staticmethod
    @login_required
    @scans_ns.marshal_with(serializers.out__new_slice)
    @scans_ns.doc(security='token')
    @scans_ns.doc(description='Returns newly created Slice.')
    @scans_ns.doc(responses={201: 'Success', 400: 'Invalid arguments'})
    def post(scan_id: ScanID) -> Any:
        """Upload Slice for given Scan."""
        image = request.files['image']
        image_data = image.read()
        new_slice = business.add_new_slice(scan_id, image_data)
        return new_slice, 201
