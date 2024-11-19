const mongoose = require('mongoose');
const Schema = mongoose.Schema;


const candidateSchema = new Schema({
    nicNumber: {
        type: String,
        required: true
    },
    Cname: {
        type: String,
        required: true
    },
    district: {
        type: String,
        required: true
    },
    districtID: {
        type: String,
        
    },
    partyname: {
        type: String,
        required: true
    },
    Number: {
        type: String,
        required: true
    }, 
    ElectionName: {
        type: String,
        required: true
    },
    Sign: {
      type: String
    },
    PersonId: { type: mongoose.Schema.Types.ObjectId, ref: 'Person' },
    
    vote_count: {
        type: Number,
        default: 0 
    },
    vote_count_option_1: {
        type: Number,
        default: 0 
    },
    vote_count_option_2: {
        type: Number,
        default: 0 
    },
    vote_count_option_3: {
        type: Number,
        default: 0
    }
});


const Candidates = mongoose.model('Candidates', candidateSchema);

module.exports = Candidates;
