const mongoose = require('mongoose');
const Schema = mongoose.Schema;


const electionSchema = new Schema({
    election_name: {
        type: String
        
    },
    date: {
      type: String
     
    },
    status: {
      type: String,
      enum: ['Upcoming', 'End'],
      default: "Upcoming"
     
    }
    
});


const election = mongoose.model('election', electionSchema);

module.exports = election;
