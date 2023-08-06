// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import {AgGridReact} from 'ag-grid-react';
import { CellValueChangedEvent, CellFocusedEvent, GridReadyEvent, SuppressKeyboardEventParams } from 'ag-grid-community';
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';
import '../../css/mitosheet.css';
import MitoCellEditor from './MitoCellEditor';

import { TAKE_SUGGESTION_KEYS, ARROW_UP_KEYS, ARROW_DOWN_KEYS } from './MitoCellEditor';

// And functions for building components
import { buildGridData, buildGridColumns } from '../data-utils/gridData';

// Import types
import { SheetJSON } from '../widget';
import { ModalInfo, ColumnSpreadsheetCodeJSON } from './Mito';
    
const MitoSheet = (props: {
    sheetJSON: SheetJSON; 
    formulaBarValue: string;
    editingColumn: string;
    columnSpreadsheetCodeJSON: ColumnSpreadsheetCodeJSON;
    sendCellValueUpdate: (column : string, newValue : string) => void; 
    setEditingMode: (on: boolean, column: string, rowIndex: number) => void;
    setModal: (modal: ModalInfo) => void;
    setEditingFormula: (formula: string) => void;
    setCursorIndex: (index: number) => void;
    cursorIndex: number;
    cellFocused: (event: CellFocusedEvent) => void;
    model_id: string;
}): JSX.Element => {
    
    function onGridReady(params: GridReadyEvent) {
        if (window.gridApiMap === undefined) {
            window.gridApiMap = new Map();
        }
        window.gridApiMap.set(props.model_id, params.api);
    }

    const cellValueChanged = (e : CellValueChangedEvent) => {
        const column = e.colDef.field ? e.colDef.field : "";
        const newValue = e.newValue;
        
        props.sendCellValueUpdate(column, newValue);
    };

    const columns = buildGridColumns(
        props.sheetJSON.columns, 
        props.columnSpreadsheetCodeJSON, 
        props.formulaBarValue,
        props.editingColumn,
        props.cursorIndex,
        props.setEditingMode, 
        props.setEditingFormula,
        props.setCursorIndex,
        props.setModal
    );
    const rowData = buildGridData(props.sheetJSON);

    const frameworkComponents = {
        simpleEditor: MitoCellEditor,
    }

    return (
        <div>
            <div className="ag-theme-alpine ag-grid"> 
                <AgGridReact
                    onGridReady={onGridReady}
                    onCellFocused={(e : CellFocusedEvent) => props.cellFocused(e)}
                    rowData={rowData}
                    frameworkComponents={frameworkComponents}
                    suppressKeyboardEvent={(params: SuppressKeyboardEventParams) => {
                        /* 
                            While we're editing a cell, we suppress events that we use
                            to do things within the editor.

                            NOTE: this function should suppress the events matched in onKeyDown
                            in MitoCellEditor!
                        */

                        if (!params.editing) {
                            return false;
                        }
                        return TAKE_SUGGESTION_KEYS.includes(params.event.key) ||
                               ARROW_UP_KEYS.includes(params.event.key) ||
                              ARROW_DOWN_KEYS.includes(params.event.key);
                    }}
                    onCellValueChanged={cellValueChanged} >
                    {columns}
                </AgGridReact>
            </div>
        </div>
    );
};

export default MitoSheet;