// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

// Import CSS
import "../../css/mito-toolbar.css"
import "../../css/margins.css"


// Import Types
import { SheetJSON } from '../widget';
import { ModalInfo, ModalEnum } from './Mito';

// Import Components 
import Tooltip from './Tooltip';

const MitoToolbar = (
    props: {
        sheetJSON: SheetJSON, 
        selectedSheetIndex: number,
        send: (msg: Record<string, unknown>) => void,
        setDocumentation: (documentationOpen: boolean) => void,
        setModal: (modal: ModalInfo) => void,
        model_id: string
    }): JSX.Element => {

    /* Adds a new column onto the end of a sheet, with A, B, C... as the name */
    const addColumn = () => {
        const newColumn = String.fromCharCode(65 + props.sheetJSON.columns.length);
        // Log the new column creation
        window.logger?.track({
            userId: window.user_id,
            event: 'button_column_added_log_event',
            properties: {
                column_header: newColumn
            }
        })
        // TODO: have to update these timestamps, etc to be legit
        props.send({
            'event': 'edit_event',
            'type': 'add_column',
            'sheet_index': props.selectedSheetIndex,
            'id': '123',
            'timestamp': '456',
            'column_header': newColumn
        })
    }

    /* Saves the current file as as an exported analysis */
    const downloadAnalysis = () => {
        window.logger?.track({
            userId: window.user_id,
            event: 'button_download_log_event',
            properties: {}
        })
        // We export using the gridApi.
        window.gridApiMap?.get(props.model_id)?.exportDataAsCsv({
            fileName: 'mito-export'
        });
        props.setModal({type: ModalEnum.Download});
    }

    const openDocumentation = () => {
        // We log the opening of the repeat documentation sidebar
        window.logger?.track({
            userId: window.user_id,
            event: 'button_documentation_log_event',
            properties: {
                stage: 'opened'
            }
        });
        props.setDocumentation(true);
    }

    const openMerge = () => {
        props.setModal({type: ModalEnum.Merge});
    }

    return (
        <div className='mito-toolbar-container'>
            <div className='mito-toolbar-item vertical-align-content'>
                <svg className='mt-p5' width="37" height="30" viewBox="0 0 16 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3.87559 7.30783L5.20063 5.79348C5.78086 5.13036 6.61911 4.74999 7.50024 4.74999L7.54982 4.74999C7.90452 4.74999 8.2447 4.60909 8.49551 4.35827C8.58744 4.26635 8.6995 4.19709 8.82283 4.15598L9.95107 3.77988C10.0721 3.73952 10.1822 3.67153 10.2724 3.58129C10.3982 3.45552 10.6021 3.45552 10.7279 3.58129L12.2894 5.14288C12.5659 5.41934 12.9859 5.40573 13.2501 5.1766L13.2501 5.50001L13.5001 5.50001L13.2501 5.50002C13.2501 5.79001 13.1826 6.07603 13.053 6.33541L12.352 7.73731C12.0198 8.40189 11.4065 8.89073 10.6843 9.07126C10.1561 9.20331 9.66907 9.47751 9.28352 9.8631C9.00842 10.1382 8.67302 10.3455 8.3039 10.4686L7.67731 10.6774C6.58871 11.0403 5.41178 11.0403 4.32317 10.6775L3.50049 10.4032C3.26025 10.3232 3.04194 10.1883 2.86285 10.0092C2.75579 9.90221 2.66414 9.7808 2.59054 9.64851L1.70334 8.05374C2.48732 8.20473 3.32111 7.94153 3.87559 7.30783Z" fill="#343434" fillOpacity="0.5" stroke="#343434" strokeWidth="0.5"/>
                    <path d="M4.64358 9.40301C3.1078 9.0887 -0.290268 8.51438 1.51538 4C2.00277 3.02543 4.25457 2.2291 7.34397 1.06467C7.4569 1.0221 7.57722 1 7.69791 1H9.01538H10.7793C10.9788 1 11.1738 1.05969 11.3391 1.17139L12.2896 1.81355C12.4687 1.93458 12.6038 2.11041 12.6746 2.31468L13.0236 3.32153C13.0644 3.43947 13.0817 3.56392 13.0898 3.68847C13.1095 3.99078 13.1736 4.40493 13.0913 4.97012C12.9842 5.70575 11.7756 6.71418 11.0529 6.88856C10.464 7.03069 9.68653 7.22013 8.68654 7.46977C8.60721 7.48957 8.52382 7.49685 8.44313 7.51008C7.99812 7.58309 7.43142 8.06263 5.43835 9.27491C5.20187 9.41876 4.91476 9.45851 4.64358 9.40301Z" fill="#0081DE" stroke="#343434" strokeWidth="0.5"/>
                    <path d="M3.08838 3.91162L6.5 7.5" stroke="#A3A3A3" strokeWidth="0.25"/>
                    <path d="M5.08838 2.91162L8 6" stroke="#A3A3A3" strokeWidth="0.25"/>
                    <path d="M7.5 2L10.5 5.50001" stroke="#A3A3A3" strokeWidth="0.25"/>
                    <path d="M3 5.49997L9.8638 1.88307" stroke="#A3A3A3" strokeWidth="0.25"/>
                    <path d="M3.50013 7.49997L10.8976 3.3306" stroke="#A3A3A3" strokeWidth="0.25"/>
                </svg>
            </div>

            <button className='mito-toolbar-item vertical-align-content' onClick={addColumn}>
                <svg width="22" height="30" viewBox="0 0 8 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.45459 1V2.81818" stroke="#343434" strokeWidth="0.7" strokeLinecap="round"/>
                    <path d="M7.36365 1.90909L5.54547 1.90909" stroke="#343434" strokeWidth="0.7" strokeLinecap="round"/>
                    <path d="M6.45455 4.18182V6.90909V10.5455C6.45455 10.7965 6.25104 11 6 11H1.45455C1.20351 11 1 10.7965 1 10.5455V1.45455C1 1.20351 1.20351 1 1.45455 1H4.8961" stroke="#343434" strokeWidth="0.7"/>
                    <rect x="1" y="4.63635" width="5.45455" height="3.63636" fill="#343434" fillOpacity="0.19"/>
                </svg>
                <Tooltip tooltip={"Add Column"}/>
            </button>

            <button className='mito-toolbar-item vertical-align-content' onClick={downloadAnalysis}>
                <svg width="22" height="25" viewBox="0 0 8 9" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M0.899994 5.89999V6.95V8H7.20001V5.89999" stroke="#343434" strokeWidth="0.7" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M4.05923 5.39774V0.999997" stroke="#343434" strokeWidth="0.7" strokeLinecap="round"/>
                    <path d="M6.51079 3.88084C6.64455 3.74129 6.63986 3.51974 6.50031 3.38598C6.36077 3.25221 6.13921 3.2569 6.00545 3.39645L6.51079 3.88084ZM4.0905 5.90001L3.8413 6.14577C3.90768 6.21308 3.99846 6.25067 4.09299 6.25C4.18752 6.24933 4.27776 6.21045 4.34317 6.14221L4.0905 5.90001ZM2.10958 3.39288C1.97385 3.25525 1.75225 3.25371 1.61462 3.38944C1.47699 3.52517 1.47545 3.74677 1.61118 3.8844L2.10958 3.39288ZM6.00545 3.39645L3.83783 5.65782L4.34317 6.14221L6.51079 3.88084L6.00545 3.39645ZM4.33971 5.65425L2.10958 3.39288L1.61118 3.8844L3.8413 6.14577L4.33971 5.65425Z" fill="#343434"/>
                </svg>
                <Tooltip tooltip={"Download Analysis"}/>
            </button>

            <button className='mito-toolbar-item' onClick={openDocumentation}>
                <svg width="25" height="25" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="7" cy="7" r="6.51" stroke="#404040" strokeWidth="0.98"/>
                    <path d="M7.27173 8.43865C7.2624 8.34531 7.2624 8.30798 7.2624 8.26131C7.2624 7.89731 7.38373 7.56131 7.67307 7.36531L8.1024 7.07598C8.64373 6.71198 9.0544 6.19865 9.0544 5.45198C9.0544 4.49998 8.31707 3.57598 7.0104 3.57598C5.57307 3.57598 4.94773 4.63065 4.94773 5.48931C4.94773 5.65731 4.9664 5.80665 5.00373 5.93731L5.90907 6.04931C5.87173 5.94665 5.84373 5.75065 5.84373 5.59198C5.84373 5.00398 6.1984 4.39731 7.0104 4.39731C7.75707 4.39731 8.12107 4.91065 8.12107 5.46131C8.12107 5.82531 7.94373 6.16131 7.6264 6.37598L7.21573 6.65598C6.66507 7.02931 6.44107 7.49598 6.44107 8.11198C6.44107 8.23331 6.44107 8.32665 6.4504 8.43865H7.27173ZM6.24507 9.77331C6.24507 10.1093 6.51573 10.38 6.85173 10.38C7.18773 10.38 7.46773 10.1093 7.46773 9.77331C7.46773 9.43731 7.18773 9.15731 6.85173 9.15731C6.51573 9.15731 6.24507 9.43731 6.24507 9.77331Z" fill="#343434"/>
                </svg>
                <Tooltip tooltip={"Documentation"}/>
            </button>

            <button className='mito-toolbar-item' onClick={openMerge}>
            <svg width="40" height="30" viewBox="0 0 23 13" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14.705 6.5C14.705 9.83244 11.5513 12.625 7.54 12.625C3.52871 12.625 0.375 9.83244 0.375 6.5C0.375 3.16756 3.52871 0.375 7.54 0.375C11.5513 0.375 14.705 3.16756 14.705 6.5Z" fill="#C8C8C8" stroke="#343434" strokeWidth="0.75"/>
                <path d="M21.9845 6.5C21.9845 9.83244 18.8308 12.625 14.8195 12.625C10.8083 12.625 7.65454 9.83244 7.65454 6.5C7.65454 3.16756 10.8083 0.375 14.8195 0.375C18.8308 0.375 21.9845 3.16756 21.9845 6.5Z" stroke="#343434" strokeWidth="0.75"/>
            </svg>
                <Tooltip tooltip={"Merge"}/>
            </button>
            {/* add className mito-toolbar-item to a div below to add another toolbar item! */}
        </div>
    );
};

export default MitoToolbar;