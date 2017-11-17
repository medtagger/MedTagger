import {SliceSelection} from './SliceSelection';

export interface ScanSelection<SliceSelection> {
  _selections: SliceSelection[];

  toJSON(): Object;
}
