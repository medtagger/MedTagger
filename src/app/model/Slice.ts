export class Slice {
  private _id: number;
  private _source: string;

  constructor( id: number, source: string) {
    this._id = id;
    this._source = source;
  }

  public get id() {
    return this._id;
  }

  public get source() {
    return this._source;
  }
}
