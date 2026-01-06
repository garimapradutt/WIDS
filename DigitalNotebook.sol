// SPDX-License-Identifier: MIT
pragma solidity ^0.8.31;

contract PersonalStorage {
    
    // Struct to store a note
    struct Note {
        string message;
        uint timestamp;
    }

    // Mapping 
    mapping(address => Note[]) private userNotes;

    // Global counter 
    uint public totalNotes;

    // Add a new note
    function addNote(string calldata _message) external {
        userNotes[msg.sender].push(
            Note({
                message: _message,
                timestamp: block.timestamp
            })
        );
        totalNotes++;
    }

    // Retrieve all notes
    function getNotes() external view returns (Note[] memory) {
        return userNotes[msg.sender];
    }
}
