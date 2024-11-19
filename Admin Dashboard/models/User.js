const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const LoginSchema = new Schema({
  name: {
    type: String,
    required: true
  },
  NIC: {
    type: String,
    required: true
  },
  email: {
    type: String,
    required: true,
    unique: true // Example of adding uniqueness to email
  },
  password: {
    type: String,
    required: true
  }
});

const User = mongoose.model('User', LoginSchema);
module.exports = User;
