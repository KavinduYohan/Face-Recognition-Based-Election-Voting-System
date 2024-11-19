const express = require('express');
const path = require('path');
const dotenv = require('dotenv');
const mongoose = require('mongoose');

const app = express();

app.use('/uploads', express.static('uploads'));

// Load environment variables from config file
dotenv.config({ path: './config.env' });

// Connect to MongoDB
mongoose.connect(process.env.mongodburl, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => {
  console.log('MongoDB connected');
})
.catch((err) => {
  console.error('MongoDB connection error:', err);
  process.exit(1); // Exit process on MongoDB connection error
});


// const methodOverride = require('method-override');
// app.use(methodOverride('_method'));

// Set the view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Middleware
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded bodies
app.use(express.json()); // Parse JSON bodies
app.use(express.static('public')); // Serve static files from 'public' directory

// Require and use router
const adminRouter = require('./routers/Admin');
app.use(adminRouter);

app.get("/", (req, res) => {
  res.render("login");
});

app.get("/signup", (req, res) => {
  res.render("signup");
});

// Start server
const port = process.env.PORT || 7500;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
