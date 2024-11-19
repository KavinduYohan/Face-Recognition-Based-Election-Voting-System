const mongoose = require('mongoose');
const Schema = mongoose.Schema;


const personSchema = new Schema({
    Name: {
        type: String,
        required: true
    },
    age: {
      type: String,
      required: true
    },
    Id: {
      type: String,
      required: true
    },
    status: {
      type: String,
      enum: ['YES', 'NO'],

    },
    fullName:{
      type: String,
    },
    birthday:{
      type: Date,
    },
    district:{
      type: String,
    },
    zonal_name:{
      type: String,
    },
    gender:{
      type: String,
    } 
});


const students = mongoose.model('students', personSchema);

module.exports = students;
