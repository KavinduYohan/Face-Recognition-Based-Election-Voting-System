const mongoose = require('mongoose');
const Schema = mongoose.Schema;


const partySchema = new Schema({
    party_name: {
        type: String
        
    },
    logo: {
      type: String
     
    },
    votes: {
      type: Number,
      default: 0 
    }
});


const party = mongoose.model('party', partySchema);

module.exports = party;
