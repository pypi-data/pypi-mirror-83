// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { ModalEnum, ModalInfo } from './Mito';

import '../../css/column-header.css';


/* 
  A custom component that AG-Grid displays for the column
  header, that we extend to open the column header popup when clicked.
*/
const ColumnHeader = (props: {
    setModal: (modal: ModalInfo) => void;
    displayName: string
  }): JSX.Element => {
    return (
      <div>
        <div 
          onClick={() => {props.setModal({type: ModalEnum.ColumnHeader, columnHeader: props.displayName})}} 
          className="column-header"
          >
            {props.displayName}
          </div>
      </div>
    )
} 

export default ColumnHeader