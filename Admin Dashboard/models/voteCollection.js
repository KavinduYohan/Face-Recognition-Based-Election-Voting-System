const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const voteSchema = new Schema({
  
  votes: [
    { 
      nic: { type: String, required: true },  
      preference: { type: Number, required: true } 
    }
  ]
});

const Vote = mongoose.model('Vote', voteSchema);
module.exports = Vote;
