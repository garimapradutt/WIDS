// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FraudStorage {

    struct FraudRecord {
        string dataHash;
        uint256 prediction;
        uint256 timestamp;
    }

    mapping(string => FraudRecord) public records;

    event RecordStored(
        string indexed dataHash,
        uint256 prediction,
        uint256 timestamp
    );

    function storeResult(string memory _hash, uint256 _prediction) public {
        records[_hash] = FraudRecord({
            dataHash: _hash,
            prediction: _prediction,
            timestamp: block.timestamp
        });

        emit RecordStored(_hash, _prediction, block.timestamp);
    }

    function getRecord(string memory _hash)
        public
        view
        returns (FraudRecord memory)
    {
        return records[_hash];
    }
}
