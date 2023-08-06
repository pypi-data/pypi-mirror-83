// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';
import { ModalEnum, ModalInfo } from './Mito';
import DefaultModal from './DefaultModal';

import { SheetJSON } from '../widget';

// import css
import "../../css/merge-modal.css"


type MergeModalProps = {
    setModal: (modalInfo: ModalInfo) => void;
    sheetJSONArray: SheetJSON[];
    dfNames: string[];
    send: (msg: Record<string, unknown>) => void,
};

type MergeModalState = {
    sheetOneIndex: number;
    sheetTwoIndex: number;
    sheetOneMergeKey: number | string,
    sheetTwoMergeKey: number | string,
};


type SuggestedKeys = {
    sheetOneMergeKey: string | number,
    sheetTwoMergeKey: string | number
}


const getSharedKeys = (sheetOneIndex: number, sheetTwoIndex: number, sheetJSONArray: SheetJSON[]): string[] => {
    // Given two sheets indexes, returns all the columns that are shared between both sheets

    const sheetOneColumnNames = sheetJSONArray[sheetOneIndex].columns;
    const sheetTwoColumnNames = sheetJSONArray[sheetTwoIndex].columns;

    const sharedKeys = sheetOneColumnNames.filter(columnName => sheetTwoColumnNames.includes(columnName)).map(columnHeader => columnHeader.toString())

    return sharedKeys;
}


const getSuggestedKeys = (sheetOneIndex: number, sheetTwoIndex: number, sheetJSONArray: SheetJSON[]): SuggestedKeys => {
    // Given two sheet indexes, reccomends a key to merge on. If there are x shared keys, then:
    // - If x.length == 1, it returns this key as reccomended.
    // - Else, it does not reccomend a key!
    
    const sharedKeys = getSharedKeys(sheetOneIndex, sheetTwoIndex, sheetJSONArray);
    const sheetOneMergeKey = sharedKeys.length === 1 ? sharedKeys[0] : sheetJSONArray[sheetOneIndex].columns[0];
    const sheetTwoMergeKey = sharedKeys.length === 1 ? sharedKeys[0] : sheetJSONArray[sheetTwoIndex].columns[0];
    return {
        sheetOneMergeKey: sheetOneMergeKey,
        sheetTwoMergeKey: sheetTwoMergeKey
    }
}

class MergeModal extends React.Component<MergeModalProps, MergeModalState> {

    constructor(props: MergeModalProps) {
        super(props);

        const sheetOneIndex = 0;
        const sheetTwoIndex = Math.min(1, props.dfNames.length - 1);
        const suggestedKeys = getSuggestedKeys(sheetOneIndex, sheetTwoIndex, props.sheetJSONArray);

        
        this.state = {
            sheetOneIndex: sheetOneIndex,
            sheetTwoIndex: sheetTwoIndex,
            sheetOneMergeKey: suggestedKeys.sheetOneMergeKey,
            sheetTwoMergeKey: suggestedKeys.sheetTwoMergeKey,
        };

        this.updateSheetOneSelection = this.updateSheetOneSelection.bind(this);
        this.updateSheetOneKeySelection = this.updateSheetOneKeySelection.bind(this);
        this.updateSheetTwoSelection = this.updateSheetTwoSelection.bind(this);
        this.updateSheetTwoKeySelection = this.updateSheetTwoKeySelection.bind(this);
        this.completeMerge = this.completeMerge.bind(this);
    }

    updateSheetOneSelection = (e: React.ChangeEvent<HTMLSelectElement>): void => {
        const newSheetIndex = parseInt(e.target.value);
        const suggestedKeys = getSuggestedKeys(newSheetIndex, this.state.sheetTwoIndex, this.props.sheetJSONArray);
        this.setState({
            sheetOneIndex: newSheetIndex,
            sheetOneMergeKey: suggestedKeys.sheetOneMergeKey,
            sheetTwoMergeKey: suggestedKeys.sheetTwoMergeKey,
        });    
    }

    updateSheetOneKeySelection = (e: React.ChangeEvent<HTMLSelectElement>): void => {
        const newSheetMergeKey = e.target.value;
        this.setState({sheetOneMergeKey: newSheetMergeKey});    
    }

    updateSheetTwoSelection = (e: React.ChangeEvent<HTMLSelectElement>): void => {
        const newSheetIndex = parseInt(e.target.value);
        const suggestedKeys = getSuggestedKeys(this.state.sheetOneIndex, newSheetIndex, this.props.sheetJSONArray);
        this.setState({
            sheetTwoIndex: newSheetIndex,
            sheetOneMergeKey: suggestedKeys.sheetOneMergeKey,
            sheetTwoMergeKey: suggestedKeys.sheetTwoMergeKey
        });
    }

    updateSheetTwoKeySelection = (e: React.ChangeEvent<HTMLSelectElement>): void => {
        const newSheetMergeKey = e.target.value;
        this.setState({sheetTwoMergeKey: newSheetMergeKey});    
    }
    
    completeMerge = (): void => {

        window.logger?.track({
            userId: window.user_id,
            event: 'button_merge_log_event',
            properties: {
                stage: 'merged',
                sheet_index_one: this.state.sheetOneIndex,
                merge_key_one: this.state.sheetOneMergeKey,
                sheet_index_two: this.state.sheetTwoIndex,
                merge_key_two: this.state.sheetTwoMergeKey
            }
        })


        this.props.send({
            'event': 'edit_event',
            'type': 'merge',
            'id': '123',
            'timestamp': '456',
            'sheet_index_one': this.state.sheetOneIndex,
            'merge_key_one': this.state.sheetOneMergeKey,
            'sheet_index_two': this.state.sheetTwoIndex,
            'merge_key_two': this.state.sheetTwoMergeKey
        })
        this.props.setModal({type: ModalEnum.None});
    }


    render()  {
        const sheetOneSelect = (
            <select className='merge-modal-sheet-dropdown' onChange={this.updateSheetOneSelection}>
                {this.props.dfNames.map((dfName, index) => {
                    return (<option key={dfName} value={index} selected={this.state.sheetOneIndex === index}>{dfName}</option>);
                })}
            </select>
        )

        const sheetOneMergeKeySelect = (
            <select className='merge-modal-key-dropdown' onChange={this.updateSheetOneKeySelection}>
                {this.props.sheetJSONArray[this.state.sheetOneIndex].columns.map((columnHeader) => {
                    return (<option key={columnHeader} value={columnHeader} selected={this.state.sheetOneMergeKey === columnHeader}>{columnHeader}</option>);
                })}
            </select>
        )
    
        const sheetTwoSelect = (
            <select className='merge-modal-sheet-dropdown' onChange={this.updateSheetTwoSelection}>
                {this.props.dfNames.map((dfName, index) => {
                    return (<option key={dfName} value={index} selected={this.state.sheetTwoIndex === index}>{dfName}</option>);
                })}
            </select>
        )

        const sheetTwoMergeKeySelect = (
            <select className='merge-modal-key-dropdown' onChange={this.updateSheetTwoKeySelection}>
                {this.props.sheetJSONArray[this.state.sheetTwoIndex].columns.map((columnHeader) => {
                    return (<option key={columnHeader} value={columnHeader} selected={this.state.sheetTwoMergeKey === columnHeader}>{columnHeader}</option>);
                })}
            </select>
        )
        
        // if there are no sheets to merge, don't try to display modal
        if (this.props.dfNames.length === 0) {
            return (
                <DefaultModal
                    header='Merge two sheets'
                    modalType={ModalEnum.Merge}
                    viewComponent= {
                        <Fragment>
                            There are no sheets to merge
                        </Fragment>
                    }
                    buttons = {
                        <Fragment>
                            <div className='modal-close-button' onClick={() => {this.props.setModal({type: ModalEnum.None})}}> Close </div>
                        </Fragment>
                    }
                />
            )
        }

        return (
            <DefaultModal
                header='Merge two sheets'
                modalType={ModalEnum.Merge}
                viewComponent= {
                    <Fragment>
                        <div className='merge-modal-content'>
                            <div className='merge-modal-sheet-and-key'>
                                <div>
                                    <p className='merge-modal-sheet-label'>
                                        First Sheet
                                    </p>
                                    {sheetOneSelect}
                                </div>
                                <div>
                                    <p className='merge-modal-key-label'>
                                        Merge Key
                                    </p>
                                    {sheetOneMergeKeySelect}
                                </div>
                            </div>
                            <div className='merge-modal-sheet-and-key'>
                                <div>
                                    <p className='merge-modal-sheet-label'>
                                        Second Sheet
                                    </p>
                                    {sheetTwoSelect}
                                </div>
                                <div>
                                    <p className='merge-modal-key-label'>
                                        Merge Key
                                    </p>
                                    {sheetTwoMergeKeySelect}
                                </div>
                            </div>  
                        </div>
                    </Fragment>
                }
                buttons = {
                    <Fragment>
                        <div className='modal-close-button modal-dual-button-left' onClick={() => {this.props.setModal({type: ModalEnum.None})}}> Close </div>
                        <div className='modal-action-button modal-dual-button-right' onClick={this.completeMerge}> {"Merge"}</div>
                    </Fragment>
                }
            />
        ); 
    }
}

export default MergeModal;