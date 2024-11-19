const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const personSchema = new Schema({
    fullName: {
        type: String,
        required: true
    },
    nameWithInitials: {
        type: String,
        required: true
    },
    birthday: {
        type: Date,
        required: true
    },
    nicNumber: {
        type: String,
        required: true
    },
    district: {
        type: String,
        required: true
    },
    photo: {
        type: String 
    },
    zonal: {
        type: String
    },
    gender: {
        type: String,
        enum: ['Male', 'Female', 'Other'], 
        required: true
    },
    zonalNumber: {
        type: String,
        required: true
    },
    
    stnum: { type: mongoose.Schema.Types.ObjectId, ref: 'students' }
});


const Person = mongoose.model('Person', personSchema);

module.exports = Person;
