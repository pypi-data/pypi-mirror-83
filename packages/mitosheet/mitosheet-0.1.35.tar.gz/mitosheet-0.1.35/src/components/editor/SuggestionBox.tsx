// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { FunctionDocumentationObject } from '../../data/function_documentation';

import '../../../css/suggestion-box.css'


/*
  The suggestion box suggests functions that you could be trying to
  type, beneath the cell editor. 
*/
const SuggestionBox = (
  props : {
    match: string,
    suggestions : Array<FunctionDocumentationObject>,
    index: number,
    onMouseEnterSuggestion: (suggestionIndex: number) => void,
    onSelectSuggestion: (startOfFunction: string, restOfFunction: string) => void
  }): JSX.Element => {

  const selectedIndex = props.index % props.suggestions.length;
    
  const functionMatchesDivs = props.suggestions.map((funcDocObject, idx) => {
    const restOfFunction = funcDocObject.function.substr(props.match.length);
    if (idx === selectedIndex) {
      return (
        <div 
          key={funcDocObject.function} 
          onMouseEnter={() => props.onMouseEnterSuggestion(idx)} 
          onClick={() => {props.onSelectSuggestion(props.match, restOfFunction)}}
            >
          <div className='suggestion-box-selected-function'>
            {funcDocObject.function}
          </div>
          <div className='suggestion-box-selected-description'>
            {funcDocObject.description}
          </div>
        </div>
      );
    } else {
      return (
        <div 
          className='suggestion-box-function'
          key={funcDocObject.function} 
          onMouseEnter={() => props.onMouseEnterSuggestion(idx)} 
          onClick={() => {props.onSelectSuggestion(props.match, restOfFunction)}}
            >
          {funcDocObject.function}
        </div>
      )
    }
  })

  return (
    <div className='suggestion-box-container'>
      {functionMatchesDivs}  
    </div>
  )    
};

export default SuggestionBox;