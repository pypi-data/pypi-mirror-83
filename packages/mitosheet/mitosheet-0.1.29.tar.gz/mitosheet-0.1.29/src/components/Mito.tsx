// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { MouseEvent } from 'react';

// Import types
import { CellFocusedEvent } from 'ag-grid-community';
import { SheetJSON, ErrorJSON } from '../widget';

// Import sheet and code components
import MitoSheet from './MitoSheet';
import SheetTab from './SheetTab';
import FormulaBar from './FormulaBar';
import MitoToolbar from './MitoToolbar';
import DocumentationSidebarContainer from './documentation/DocumentationSidebarContainer';

// Import modals
import ErrorModal from './ErrorModal';
import DownloadModal from './DownloadModal';
import RepeatAnalysisModal from './RepeatAnalysisModal';
import ColumnHeaderModal from './modals/ColumnHeaderModal';
import MergeModal from './MergeModal';

// Import css
import "../../css/mito.css"

export interface ColumnSpreadsheetCodeJSON {
    [Key: string]: string;
}

export enum ModalEnum {
    None = 'None',
    Error = 'Error',
    RepeatAnalysis = 'RepeatAnalysis',
    Download = 'Download',
    ColumnHeader = 'ColumnHeader',
    Merge = 'Merge'
}

/* 
    Each modal comes with modal info, and we enforce (through types) that if you set
    the current modal, you must also pass it the data that it requires. 

    To see what information a modal requires, see it's <>ModalInfo type definition
    below!

    NOTE: Currently, the column header modal is the only modal that needs any data...
    but this is a good investment for the future :)
*/
interface NoneModalInfo {type: ModalEnum.None}
interface ErrorModalInfo {type: ModalEnum.Error}
interface RepeatAnalysisModalInfo {type: ModalEnum.RepeatAnalysis}
interface DownloadModalInfo {type: ModalEnum.Download}
interface MergeModalInfo {type: ModalEnum.Merge}
interface ColumnHeaderModalInfo {
    type: ModalEnum.ColumnHeader;
    columnHeader: string;
}

export type ModalInfo = 
    | NoneModalInfo 
    | ErrorModalInfo
    | RepeatAnalysisModalInfo
    | DownloadModalInfo
    | MergeModalInfo
    | ColumnHeaderModalInfo


type MitoProps = {
    dfNames: string[];
    columnSpreadsheetCodeJSONArray: ColumnSpreadsheetCodeJSON[];
    sheetJSONArray: SheetJSON[];
    send: (msg: Record<string, unknown>) => void
    model_id: string;
};

type MitoState = {
    dfNames: string[];
    columnSpreadsheetCodeJSONArray: ColumnSpreadsheetCodeJSON[];
    sheetJSONArray: SheetJSON[];
    selectedSheetIndex: number;
    formulaBarValue: string;
    lastFormula: string; // This is the last formula there is, and it notably might be invalid
    selectedColumn: string;
    selectedRowIndex: number;
    errorJSON: ErrorJSON;
    editingModeOn: boolean;
    editingCellColumn : string;
    editingCellRowIndex : number;
    documentationOpen: boolean;
    modalInfo: ModalInfo;
};

const INDEX_COLUMN = "index";


class Mito extends React.Component<MitoProps, MitoState> {

    constructor(props: MitoProps) {
        super(props);

        this.state = {
            dfNames: this.props.dfNames,
            columnSpreadsheetCodeJSONArray: this.props.columnSpreadsheetCodeJSONArray,
            sheetJSONArray: this.props.sheetJSONArray,
            selectedSheetIndex: 0,
            formulaBarValue: this.props.sheetJSONArray[0].data[0][0],
            lastFormula: this.props.sheetJSONArray[0].data[0][0],
            selectedColumn: this.props.sheetJSONArray[0].columns[0].toString(),
            selectedRowIndex: 0,
            /*
                we tell if we're in cell editing mode through the editingModeOn state variable

                the editingCellColumn and editingCellRowIndex are used to update the formula of the correct
                cell editor. They get set to the new values when we turn cell editing mode back on, but are unchanged
                when we turn cell editing mode off so that we can handle formulas that error by letting the user 
                edit the formula that they submitted. 
            */
            editingModeOn: false,
            editingCellColumn: "",
            editingCellRowIndex: -1,
            documentationOpen: false,
            errorJSON: {
                event: '',
                type: '',
                header: '',
                to_fix: ''
            },
            modalInfo: {type: ModalEnum.None}
        };

        this.cellFocused = this.cellFocused.bind(this);
        this.handleFormulaBarDoubleClick = this.handleFormulaBarDoubleClick.bind(this);
        this.sendCellValueUpdate = this.sendCellValueUpdate.bind(this);
        this.setEditingMode = this.setEditingMode.bind(this);
        this.setEditingFormula = this.setEditingFormula.bind(this);
        this.setDocumentation = this.setDocumentation.bind(this);
        this.setModal = this.setModal.bind(this);
        this.getCurrentModalComponent = this.getCurrentModalComponent.bind(this);
        this.setSelectedSheetIndex = this.setSelectedSheetIndex.bind(this);
        this.turnOnCellEditor = this.turnOnCellEditor.bind(this);
    }

    /* 
        This function is responsible for turning cell editing mode on and off
        by setting the state of editingCellColumn, and editingCellRowIndex.

        If you call this function with on===true, then the passed column and rowIndex
        should be the cell you want to start editing.

        If you call this function with on===false, then editing will be stopped, and the 
        passed column and rowIndex will be focused on.
    */
   
    setEditingMode(on: boolean, column: string, rowIndex: number) : void {
        if (on && !this.state.editingModeOn) {
            /* 
                This runs (and turns on editing mode) when we're not in editing mode and:
                1. The user double clicks on a cell
                2. The user presses enter on a cell. 
                3. The user types any character on a cell. 
            */

            this.setState({
                editingModeOn: true,
                editingCellColumn: column,
                editingCellRowIndex: rowIndex
            });
        } else if (!on) {
            /* 
                We turn off cell-editing mode and select the given cell.

                This handles some of the many ways cell editing can be stopped
                explicitly (e.g. ENTER), as we want only sometimes want ENTER to stop 
                editing (in other cases, we want it to select a suggestion!).

                To see a list of events that stop editing, see:
                https://www.ag-grid.com/javascript-grid-cell-editing/#stop-end-editing
            */
            this.setState({
                editingModeOn: false,
            });

            // We actually stop the grid from editing in this case, and set cell focus
            // as stopping editing focuses on nothing by default.
            window.gridApiMap?.get(this.props.model_id)?.stopEditing();
            window.gridApiMap?.get(this.props.model_id)?.setFocusedCell(
                rowIndex, 
                column
            );
        }
    }

    /*
        This function is called by the cell editor to update the formula of the editing cell
        in the mito state, so that when cellFocused starts editing mode again, it can 
        pass in the starting formula.  

        We save the formula in the state because:
            1) when the user clicks on another cell, it closes the cell editor.
            We need to store the formula in state so when we put the editor 
            back in cell editing mode in the CellFocussedEvent, 
            we're able to start the cell editor with the correct formula. 
            
            Note: we don't want to send the intermediate formula to the parser

            2) we need to display the formula that is in the editor in the formula bar as well.  
    */
    setEditingFormula(formula : string) : void {
        this.setState({
            formulaBarValue: formula,
            lastFormula: formula
        });
    }

    turnOnCellEditor () : void {
        const editingModeParams = {
            rowIndex: this.state.editingCellRowIndex,
            colKey: this.state.editingCellColumn,
        }

        // turn the editing cell's cell editor back on!
        window.gridApiMap?.get(this.props.model_id)?.startEditingCell(editingModeParams);
    }

    /* 
        Occurs when a cell is clicked. If we are currently editing a cell, we append the clicked
        column to the currently-edited cell. Otherwise, we select the clicked cell.
    */
    cellFocused(event : CellFocusedEvent) : void {
        /* 
            We avoid cell focused throwing an error when switching sheets by making sure the 
            event is defined, and just returning. Not sure why this occurs!

            Additionally, turn of cell editing mode & reset the formulaBarValue. when the user switches
            sheets we reset the editing cell to clear the formula bar
        */
        const column = event.column?.getColId();
        if (!column) {
            this.setEditingMode(false, "", -1);
            this.setState({
                formulaBarValue: '',
                editingCellColumn: '',
                editingCellRowIndex: -1
            });
            return;
        } 

        // if we're in cell editing mode, turn cell editor back on
        if (this.state.editingModeOn) {

            /* 
                if the column we focussed on is the editing column or the index column, don't append to the formula
            */ 
            if (column === this.state.editingCellColumn || column === INDEX_COLUMN) {
                this.turnOnCellEditor();
                return;
            }

            /*
                If we're in editing mode & the cell focused on is not in the column we're editing
                or the index column, append the clicked column to the editing formula;
            */ 
            this.setState((prevState) => {
                return {
                    formulaBarValue: prevState.formulaBarValue + column,
                    lastFormula: prevState.lastFormula + column
                }
            }, () => {
                this.turnOnCellEditor()
            });
        } else {
            // If we're not in editing mode, then we update the formula bar only

            // if the column is the index column, then we reset the selected cell state
            if (column === INDEX_COLUMN) {
                this.setState({
                    selectedColumn: '',
                    selectedRowIndex: 0,
                    formulaBarValue: ''
                });
                return;
            }

            // otherwise, get the cell's formula to display
            const columnIndex = this.state.sheetJSONArray[this.state.selectedSheetIndex].columns.indexOf(column);
            const rowIndex = event.rowIndex;

            const columnFormula = this.state.columnSpreadsheetCodeJSONArray[this.state.selectedSheetIndex][column];

            let formulaBarValue = this.state.formulaBarValue;

            if (columnFormula === '') {
                // If there no formula, we just display the value
                formulaBarValue = this.state.sheetJSONArray[this.state.selectedSheetIndex].data[rowIndex][columnIndex];
            } else {
                // Otherwise, we display the formula that is in the column
                formulaBarValue = columnFormula;
                if (column === this.state.editingCellColumn) {
                    // The last formula is always equal to the _last_ edit made to a formula
                    // and so we take it so we keep an error formula
                    formulaBarValue = this.state.lastFormula;
                }
            }

            this.setState({
                selectedColumn: column,
                selectedRowIndex: rowIndex,
                formulaBarValue: formulaBarValue
            });
        }
    }

    handleFormulaBarDoubleClick(e : MouseEvent<HTMLButtonElement>) : void {
        e.preventDefault();

        /*
            when the formula bar is double clicked, turns on cell editing mode and opens the 
            selected cell's cell editor 

            TODO: make sure it works with multiple sheets. fix: when we switch sheets, 
            reset this.state.selectedColumn & this.state.selectedRowIndex
        */

        // do nothing if the selected cell is a data column
        if (this.state.columnSpreadsheetCodeJSONArray[this.state.selectedSheetIndex][this.state.selectedColumn] === '') {
            return
        }

        // turn cell editing mode on
        this.setEditingMode(true, this.state.selectedColumn, this.state.selectedRowIndex)

        /* 
            turns on the correct cell editor. If the selected cell is not in view, 
            the spreadsheet will be scrolled automatically until it is. 
        */
        const editingModeParams = {
            rowIndex: this.state.selectedRowIndex,
            colKey: this.state.selectedColumn,
        }
        window.gridApiMap?.get(this.props.model_id)?.startEditingCell(editingModeParams);
    }

    // TODO: this event should be broken out into a formula edit and a value edit
    sendCellValueUpdate(column : string, newValue : string) : void {
        /*
            We don't send the formula to the evaluator while in cell editing mode
            because this function gets called after the CellValueChangedEvent fires 
            each time the cell editor is closed. 
            
            However, the cell editor closes each time the user uses their mouse 
            to reference another column - which isn't a finished update yet!
        */
        if (!this.state.editingModeOn) {
            this.props.send({
                'event': 'edit_event',
                'type': 'cell_edit',
                'sheet_index': this.state.selectedSheetIndex,
                'id': '123',
                'timestamp': '456',
                'address': column,
                'new_formula': newValue
            });
        }
    }

    setDocumentation(documentationOpen: boolean) : void {
        this.setState({documentationOpen: documentationOpen});
    }

    getCurrentModalComponent(): JSX.Element {
        // Returns the JSX.element that is currently, open, and is used
        // in render to display this modal
        switch(this.state.modalInfo.type) {
            case ModalEnum.None: return <div></div>;
            case ModalEnum.Error: return (
                <ErrorModal
                    errorJSON={this.state.errorJSON}
                    setModal={this.setModal}
                    />
            )
            case ModalEnum.RepeatAnalysis: return (
                <RepeatAnalysisModal
                    setModal={this.setModal}
                    />
            )
            case ModalEnum.Download: return (
                <DownloadModal
                    setModal={this.setModal}
                    />
            )
            case ModalEnum.ColumnHeader: return (
                <ColumnHeaderModal
                    setModal={this.setModal}
                    send={this.props.send}
                    columnHeader={this.state.modalInfo.columnHeader}
                    selectedSheetIndex={this.state.selectedSheetIndex} />
            )
            case ModalEnum.Merge: return (
                <MergeModal
                    setModal={this.setModal}
                    sheetJSONArray={this.state.sheetJSONArray}
                    dfNames={this.state.dfNames}
                    send={this.props.send}
                    />
            )
        }
    }

    setModal(modalInfo: ModalInfo) : void {
        this.setState({modalInfo: modalInfo});
    }

    setSelectedSheetIndex(newIndex: number): void {
        this.setState({selectedSheetIndex: newIndex});
    }

    // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
    render() {
                            
        return (
            <div className="mito-container">
                <div className="mitosheet">
                    <MitoToolbar 
                        sheetJSON={this.state.sheetJSONArray[this.state.selectedSheetIndex]} 
                        selectedSheetIndex={this.state.selectedSheetIndex}
                        send={this.props.send}
                        setDocumentation={this.setDocumentation}
                        setModal={this.setModal}
                        model_id={this.props.model_id}
                        />
                    <FormulaBar
                        formulaBarValue={this.state.formulaBarValue}
                        handleFormulaBarDoubleClick={this.handleFormulaBarDoubleClick} 
                    />
                    <MitoSheet 
                        formulaBarValue={this.state.formulaBarValue} 
                        editingColumn={this.state.editingCellColumn}
                        columnSpreadsheetCodeJSON={this.state.columnSpreadsheetCodeJSONArray[this.state.selectedSheetIndex]}
                        sheetJSON={this.state.sheetJSONArray[this.state.selectedSheetIndex]} 
                        setEditingMode={this.setEditingMode}
                        setModal={this.setModal}
                        setEditingFormula={this.setEditingFormula}
                        cellFocused={this.cellFocused}
                        model_id={this.props.model_id}
                        sendCellValueUpdate={this.sendCellValueUpdate} 
                        />
                    <div className="sheet-tab-bar">
                        {this.state.sheetJSONArray.map((sheetJSON, index) => {
                            // If we can't get the df name, we just call it df{index}!
                            const sheetName = this.state.dfNames[index] ? this.state.dfNames[index] : `df${index + 1}`
                            return (
                                <SheetTab 
                                    key={sheetName}
                                    sheetName={sheetName}
                                    sheetIndex={index}
                                    selectedSheetIndex={this.state.selectedSheetIndex}
                                    setSelectedSheetIndex={this.setSelectedSheetIndex} />
                            )
                        })}
                    </div>
                </div>
                {this.getCurrentModalComponent()}
                {this.state.documentationOpen && 
                    <div className="sidebar">
                        <DocumentationSidebarContainer setDocumentation={this.setDocumentation}/>
                    </div>
                }                
            </div>
        );
    }

}


export default Mito;