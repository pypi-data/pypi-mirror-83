// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment, useState } from 'react';
import { ModalEnum, ModalInfo } from './Mito';
import DefaultModal from './DefaultModal';

// import css
import "../../css/margins.css"


/*
    A modal that allows users to input a file path to 
    repeat the current analysis on that file, in a
    new Jupyter code cell.
*/
const RepeatAnalysisModal = (props : {setModal: (modalInfo: ModalInfo) => void}): JSX.Element => {
    const [fileName, setFileName] = useState('');

    function repeatAnalysis() : void {
        window.logger?.track({
            userId: window.user_id,
            event: 'button_repeat_analysis_log_event',
            properties: {
                stage: 'repeated',
                fileName: fileName
            }
        })
        window.commands?.execute('repeat-analysis', {fileName: fileName});
        props.setModal({type: ModalEnum.None});
    }

    return (
        <DefaultModal
            header='Repeat analysis'
            modalType={ModalEnum.RepeatAnalysis}
            viewComponent= {
                <Fragment>
                    <div className="mt-2">
                        <p>
                            Select a csv file to repeat your analysis on.
                        </p>
                        <input 
                            className="mt-2 modal-input"
                            type="text" 
                            placeholder='datafile2.csv' 
                            value={fileName} 
                            onChange={(e) => {setFileName(e.target.value)}} 
                        />
                    </div>
                </Fragment>
            }
            buttons = {
                <Fragment>
                    <div className='modal-close-button modal-dual-button-left' onClick={() => {props.setModal({type: ModalEnum.None})}}> Close </div>
                    <div className='modal-action-button modal-dual-button-right' onClick={() => {repeatAnalysis()}}> {"Repeat Analysis"}</div>
                </Fragment>
            }
        />
    );
};

export default RepeatAnalysisModal;