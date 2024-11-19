const mongoose = require('mongoose');
const Schema = mongoose.Schema;


const ballotSchema = new Schema({
    candidate_nic1: {
        type: String
        
    },
    candidate_nic2: {
      type: String
     
    },
    candidate_nic3: {
      type: String
      
    }
    
});


const ballots = mongoose.model('ballots', ballotSchema);

module.exports = ballots;
