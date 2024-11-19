const mongoose = require('mongoose');
const Schema = mongoose.Schema;


const ballotSchema = new Schema({
    party: {
        type: String,
        required: true
    },
    candidate_nic1: {
        type: String,
        required: true
    },
    candidate_nic2: {
        type: String,
        required: true
    },
    candidate_nic3: {
        type: String 
    },
    created_at: {
        type: Date
       
    }
}, { collection: 'ballotsP' });


const Ballotp = mongoose.model('Ballotp', ballotSchema);

module.exports = Ballotp;
