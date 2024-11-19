const express = require('express');
const router = express.Router();
let Person = require("../models/Person.js");
let Candidates = require("../models/Candidates.js");
let Vote = require("../models/voteCollection.js");
let students = require("../models/students.js");
let User = require("../models/User.js");
let Ballot = require('../models/ballots.js');
const Ballotp = require('../models/ballotsP.js');
let Election = require('../models/election.js');
let Party = require('../models/party.js');
const multer = require('multer');
let path = require('path');

const csvParser = require('csv-parser');
const fs = require('fs');



const storage = multer.diskStorage({
  destination: function (req, file, cb) {
      cb(null, 'uploads/'); // Destination folder for uploaded files
  },
  filename: function (req, file, cb) {
      cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({ storage: storage });

router.post('/adminpanel', async (req, res) => {
  try {
      // Extract memberId from the request body
      const memberId = req.body.memberId;

      // Create a new Person document using data from the request body
      const newPerson = new Person({
          fullName: req.body.fullName,
          nameWithInitials: req.body.nameWithInitials,
          birthday: req.body.birthday,
          nicNumber: req.body.nicNumber,
          district: req.body.district,
          photo: req.body.photo,
          zonal: req.body.zonal,
          gender: req.body.gender,
          zonalNumber: req.body.zonalNumber,
          stnum: memberId // Assign memberId to the stnum field
      });

      // Save the new Person document to the database
      const savedPerson = await newPerson.save();
      res.status(201).send("Voter added successfully"); 
  } catch (err) {
      res.status(400).json({ message: err.message }); 
  }
});



router.post('/uploadCandidates', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).send('No file uploaded.');
  }

  const results = [];
  fs.createReadStream(req.file.path)
    .pipe(csvParser())
    .on('data', (data) => results.push(data))
    .on('end', async () => {
      try {
        await Candidates.insertMany(results);
        res.status(200).send('Candidates uploaded successfully.');
      } catch (err) {
        console.error('Error inserting candidates:', err);
        res.status(500).send('Error inserting candidates.');
      } finally {
        fs.unlinkSync(req.file.path); // Clean up the uploaded file
      }
    });
});

router.post('/uploadStudent', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).send('No file uploaded.');
  }

  const results = [];
  fs.createReadStream(req.file.path)
    .pipe(csvParser())
    .on('data', (data) => results.push(data))
    .on('end', async () => {
      try {
        await students.insertMany(results);
        res.status(200).send('Voter uploaded successfully.');
      } catch (err) {
        console.error('Error inserting candidates:', err);
        res.status(500).send('Error inserting Voters.');
      } finally {
        fs.unlinkSync(req.file.path); // Clean up the uploaded file
      }
    });
});



router.get('/uploadCandidates', async (req, res) => {
  // Your route handler logic here
  res.render('uploadCandidates');
});

router.get('/AddCandidates', async (req, res) => {
  // Your route handler logic here
  res.render('AddCandidates');
});
  

router.get('/showCandidates', async (req, res) => {
  try {
    // Fetch empData from your database or another source
    const empData = await Candidates.find({ ElectionName: "Presidental" });

    // Render the view and pass empData as a variable to the view
    res.render('showCandidates', { empData }); // Passing empData to the view
  } catch (err) {
    console.error('Error fetching candidates:', err);
    res.status(500).send('Error fetching candidates');
  }
});

router.get('/addcandidatespl', async (req, res) => {
  try {
    // Fetch empData from your database or another source
    const empData = await Candidates.find({ ElectionName: "Parliament" });

    // Render the view and pass empData as a variable to the view
    res.render('addcandidatespl', { empData }); // Passing empData to the view
  } catch (err) {
    console.error('Error fetching candidates:', err);
    res.status(500).send('Error fetching candidates');
  }
});



router.post('/reset/:id', async (req, res) => {
  const candidateId = req.params.id;

  try {
    // Find the candidate by _id
    const candidate = await Candidates.findById(candidateId);

    if (!candidate) {
      return res.status(404).send('Candidate not found');
    }

    // Reset vote_count to default value (0)
    candidate.vote_count_option_1 = 0;
    candidate.vote_count_option_2 = 0;
    candidate.vote_count_option_3 = 0;

    // Save the updated candidate document
    await candidate.save();

    res.status(200).send('Vote count reset successfully');
  } catch (error) {
    console.error('Error resetting vote count:', error);
    res.status(500).send('Internal Server Error');
  }
});



router.get('/controlPanel', async (req, res) => {
  // Your route handler logic here
  res.render('controlPanel');
});


  

router.get('/results', async (req, res) => {
  try {
    const candidates = await Candidates.find({ ElectionName: 'Presidental' }); // Fetch all candidates from the Candidates model

    // Calculate total votes for option 1
    let totalVotesOption1 = candidates.reduce((total, candidate) => {
      return total + candidate.vote_count_option_1;
    }, 0);

    // Calculate percentage for each candidate
    candidates.forEach(candidate => {
      candidate.votePercentageOption1 = totalVotesOption1 > 0 ? (candidate.vote_count_option_1 / totalVotesOption1) * 100 : 0;
    });

    // Find the candidate with the maximum vote_count_option_1
    let maxVotesCandidate = candidates.reduce((prev, current) => {
      return (prev.vote_count_option_1 > current.vote_count_option_1) ? prev : current;
    });

    // Calculate the percentage of the maximum votes
    let maxVotesPercentage = (maxVotesCandidate.vote_count_option_1 / totalVotesOption1) * 100;

    // Determine selection status
    let selectionStatus = maxVotesPercentage > 50 ? "selected" : "not selected";

    res.render('results', { candidates, maxVotesCandidate, totalVotesOption1, maxVotesPercentage, selectionStatus });
  } catch (err) {
    console.error('Error fetching candidates:', err);
    res.status(500).send('Error fetching candidates');
  }
});

async function populateVotes() {
  try {
    // Check if votes collection is empty
    const voteCount = await Vote.countDocuments();
    if (voteCount === 0) {
      // Fetch all candidates
      const candidates = await Candidates.find();

      // Create vote documents for each candidate
      const votePromises = candidates.map(candidate => {
        return new Vote({
          candidate: candidate._id
        }).save();
      });

      // Wait for all vote documents to be saved
      await Promise.all(votePromises);

      console.log('Votes have been populated successfully.');
    }
  } catch (err) {
    console.error('Error populating votes:', err);
  }
}


router.post('/votes', async (req, res) => {
  try {
    const {  nics, preferences } = req.body;

    // Create the votes array
    const votes = nics.map((nic, index) => ({
      nic: nic,
      preference: parseInt(preferences[index], 10)
    }));

    const voteData = {
      votes: votes
    };

    const newVote = new Vote(voteData);

    await newVote.save();

    res.send('Vote submitted successfully');
  } catch (err) {
    res.status(500).send('Error saving vote');
  }
});


router.get('/votes', async (req, res) => {
  // Your route handler logic here
  res.render('votes');
});

router.get('/votesS', async (req, res) => {
  try {
    const votes = await Vote.find();
    res.render('votesS', { votes });
  } catch (err) {
    res.status(500).send('Error fetching votes');
  }
});




router.get('/edit/:id', async (req, res) => {
  try {
      const memberId = req.params.id;
      console.log(memberId)
      // Fetch member data by memberId from the database
      // Example: Fetch from your Person model assuming you have one
      const member = await students.findById(memberId);
      console.log(member)
      if (!member) {
          return res.status(404).json({ message: 'Member not found' });
      }
      // Render adminpanel.ejs with member data
      res.render('adminpanel', { memberId: memberId });
  } catch (err) {
      res.status(500).json({ message: err.message });
  }
});

router.get('/showStudent', async (req, res) => {
  try {
    // Fetch members from your database or any other source
    const members = await students.find(); // Example using Mongoose, adjust as per your setup

    // Render the EJS template and pass the members data to it
    res.render('showStudent', { members: members }); // Ensure 'members' is defined and passed correctly
  } catch (err) {
    res.status(500).json({ message: err.message }); // Handle errors appropriately
  }
});



router.get('/ballotCollection', async (req, res) => {
  try {
      const ballots = await Ballot.find(); // Fetch all ballots
      res.render('ballotCollection', { ballots }); // Pass ballots to the view
  } catch (err) {
      console.error('Error fetching ballots:', err);
      res.status(500).send('Error fetching ballots');
  }
});

router.get('/ballotCollectionP', async (req, res) => {
  try {
    const ballotsp = await Ballotp.find();
    if (!ballotsp.length) {
      console.log('No ballots found in the database.');
    } else {
      console.log('Ballots found:', ballotsp);
    }
    res.render('ballotp', { ballotsp });
  } catch (err) {
    console.error('Error fetching ballots:', err);
    res.status(500).send('Error fetching ballots');
  }
});

router.get('/vote-results', async (req, res) => {
  try {
    // Fetch all student documents from the Students model
    const student = await students.find();
    
    if (!student || student.length === 0) {
      return res.status(404).send('No students found');
    }

    // Calculate total "YES" and "NO" statuses
    let totalYesVotes = 0;
    let totalNoVotes = 0;

    student.forEach(student => {
      if (student.status === "YES") {
        totalYesVotes++;
      } else if (student.status === "NO") {
        totalNoVotes++;
      }
    });

    const totalVotes = totalYesVotes + totalNoVotes;

    // Calculate percentages for "YES" and "NO" statuses
    const yesPercentage = totalVotes > 0 ? (totalYesVotes / totalVotes) * 100 : 0;
    const noPercentage = totalVotes > 0 ? (totalNoVotes / totalVotes) * 100 : 0;

    // Render the vote-results view with the calculated data and student details
    res.render('vote-results', {
      totalYesVotes,
      totalNoVotes,
      yesPercentage: yesPercentage.toFixed(2),
      noPercentage: noPercentage.toFixed(2),
      student // Pass student data to the view
    });
  } catch (err) {
    console.error('Error fetching students:', err);
    res.status(500).send('Error fetching students');
  }
});




router.get('/parliment', async (req, res) => {
  try {
    // Fetch empData from your database or another source with ElectionName: "Parliament"
    const empData = await Candidates.find({ ElectionName: "Parliament" });

    // Render the view and pass empData as a variable to the view
    res.render('parliment', { empData }); // Passing empData to the view
  } catch (err) {
    console.error('Error fetching candidates:', err);
    res.status(500).send('Error fetching candidates');
  }
});


router.get('/elections', async (req, res) => {
  // Your route handler logic here
  res.render('elections');
});

router.get('/presidential', async (req, res) => {
  // Your route handler logic here
  res.render('presidential');
});

router.get('/parli', async (req, res) => {
  // Your route handler logic here
  res.render('parli');
});
// Login Route
router.post("/login", async (req, res) => {
  const { email, password } = req.body;

  // Basic validation
  if (!email || !password) {
    return res.status(400).send("Email and password are required");
  }

  try {
    const user = await User.findOne({ email });

    if (!user) {
      return res.status(404).send("User not found");
    }

    if (password === user.password) {
      // Fetch election data
      const elections = await Election.find({});

      // Render the election page with data
      res.render('election', { election: elections });
    } else {
      res.status(401).send("Invalid credentials");
    }
  } catch (error) {
    console.error(error);
    res.status(500).send("Internal Server Error");
  }
});



router.post('/signup', async (req, res) => {
  const { name, NIC, email, password } = req.body;

  try {
    // Check if the email already exists
    const existingUser = await User.findOne({ email });

    if (existingUser) {
      return res.status(400).send('<script>alert("Email already exists"); window.history.back();</script>');
    }

    // Create a new user instance
    const newUser = new User({
      name,
      NIC,
      email,
      password
    });

    // Save the user to the database
    await newUser.save();

    res.status(201).send('<script>alert("User registered successfully"); window.location.href = "/";</script>');
  } catch (error) {
    res.status(500).send(`<script>alert("${error.message}"); window.history.back();</script>`);
  }
});


router.post('/add', async (req, res) => {
  try {
    const { election_name, date, candidate_nic3 } = req.body;

    const newElection = new Election({ election_name, date, candidate_nic3 });
    await newElection.save();

    res.redirect('/election');
  } catch (err) {
    console.error(err); // Log the error for debugging
    res.status(500).send('Server Error');
  }
});

// router.get('/election', async (req, res) => {
//   // Your route handler logic here
//   res.render('election');
// });

router.get('/election', async (req, res) => {
  try {
    const election = await Election.find({});
    res.render('election', { election });
  } catch (err) {
    res.status(500).send('Server Error');
  }
});

router.post('/delete/:id', async (req, res) => {
  try {
    await Election.findByIdAndDelete(req.params.id);
    res.redirect('/election');
  } catch (err) {
    console.error(err);
    res.status(500).send("Server Error");
  }
});


router.post('/addparty', upload.single('logo'), async (req, res) => {
  try {
    const { party_name } = req.body;
    const logo = req.file ? req.file.filename : '';

    // Create a new party document
    const newParty = new Party({
      party_name: party_name,
      logo: logo
    });

    // Save the party document to the database
    await newParty.save();

    res.status(200).send('Party add successfully');
  } catch (error) {
    res.status(200).send('Party add unsuccessfully');
  }
});

router.get('/addparty', async (req, res) => {
  try {
      // Fetch all parties from the database
      const parties = await Party.find({});
      res.render('addparty', { parties });
  } catch (error) {
      console.error('Error fetching parties:', error);
      res.status(500).send('Server Error');
  }
});




router.get('/resultpl', async (req, res) => {
  try {
    // Fetch all parties and candidates
    const parties = await Party.find({});
    const candidates = await Candidates.find({});
    console.log(candidates)

    // Initialize an array to store results
    const results = [];

    // Iterate through each party
    parties.forEach(party => {
      const partyName = party.party_name;
      const partyResult = {
        party_name: partyName,
        candidates: []
      };

      // Filter candidates belonging to the current party
      const partyCandidates = candidates.filter(candidate => candidate.partyname === partyName);

      // Count votes for each candidate number (N1, N2, ..., N6)
      for (let i = 1; i <= 6; i++) {
        const numberKey = `N${i}`;
        const count = partyCandidates.reduce((total, candidate) => {
          if (candidate.Number === numberKey) {
            return total + party[numberKey];
          } else {
            return total;
          }
        }, 0);

        // Find candidate name for the current candidate number
        const candidate = partyCandidates.find(candidate => candidate.Number === numberKey);

        // Push candidate count to party result
        partyResult.candidates.push({
          candidate_number: numberKey,
          candidate_name: candidate ? candidate.Cname : 'Unknown', // Display candidate name or 'Unknown'
          vote_count: count
        });
      }

      // Push party result to the main results array
      results.push(partyResult);
    });

    // Render the resultpl template with elections and results data
    res.render('resultpl', { elections: [], results: results }); // Pass empty array for elections if not used
  } catch (err) {
    console.error(err);
    res.status(500).send('Server Error');
  }
});

router.get('/presults', async (req, res) => {
  try {
    const party = await Party.find({});
    const candi = await Candidates.find({ ElectionName: 'Parliament' });    
    res.render('presults', { party, candi });
  } catch (err) {
    res.status(500).send('Server Error');
  }
});

router.get('/SLmap', async (req, res) => {
  // Your route handler logic here
  res.render('SLmap');
});

router.get('/Kandy', async (req, res) => {
  // Your route handler logic here
  res.render('Kandy');
});

router.get('/login', async (req, res) => {
  // Your route handler logic here
  res.render('login');
});



router.get('/additional_calculation', async (req, res) => {
  try {
    // Fetch all candidates from the database
    const candidatesData = await Candidates.find({});
    
    // Create a mapping between candidate NIC and candidate name
    const candidateMap = {};
    candidatesData.forEach(candidate => {
        candidateMap[candidate.nicNumber] = candidate.Cname; // Assuming Cname is the candidate's name
    });
    
    const ballotPapers = await Ballot.find({});
    const voteCounts = {};

    // Tally votes for each candidate (first round)
    ballotPapers.forEach(ballot => {
        if (ballot.candidate_nic1) {
            voteCounts[ballot.candidate_nic1] = (voteCounts[ballot.candidate_nic1] || 0) + 1;
        }
        if (ballot.candidate_nic2) {
            voteCounts[ballot.candidate_nic2] = (voteCounts[ballot.candidate_nic2] || 0) + 1;
        }
        if (ballot.candidate_nic3) {
            voteCounts[ballot.candidate_nic3] = (voteCounts[ballot.candidate_nic3] || 0) + 1;
        }
    });

    // Calculate the total number of votes
    const totalVotes = Object.values(voteCounts).reduce((sum, votes) => sum + votes, 0);

    // Convert vote counts to percentages and use candidate names
    const candidates = Object.keys(voteCounts).map(candidateNic => {
        return {
            name: candidateMap[candidateNic] || candidateNic, // Use name from the map or fallback to NIC
            votes: voteCounts[candidateNic],
            percentage: ((voteCounts[candidateNic] / totalVotes) * 100).toFixed(2)
        };
    });

    // Sort candidates by percentage in descending order
    candidates.sort((a, b) => b.votes - a.votes);

    // Check if any candidate has more than 50% of the votes
    let result;
    if (candidates[0].percentage > 50) {
        result = `${candidates[0].name} is the winner with ${candidates[0].percentage}% of the votes.`;
    } else {
        // If no candidate wins, calculate the runoff between the top 2 candidates
        const topTwo = [candidates[0].name, candidates[1].name];
        let runoffVotes = { [candidates[0].name]: 0, [candidates[1].name]: 0 };

        // Redistribute votes from the third candidate
        ballotPapers.forEach(ballot => {
            if (topTwo.includes(candidateMap[ballot.candidate_nic1])) {
                runoffVotes[candidateMap[ballot.candidate_nic1]] += 1; // First choice vote remains
            } else if (topTwo.includes(candidateMap[ballot.candidate_nic2])) {
                runoffVotes[candidateMap[ballot.candidate_nic2]] += 1; // Second choice vote redistributes
            } else if (topTwo.includes(candidateMap[ballot.candidate_nic3])) {
                runoffVotes[candidateMap[ballot.candidate_nic3]] += 1; // Third choice vote redistributes
            }
        });

        // Determine the winner from the runoff
        const runoffTotalVotes = runoffVotes[topTwo[0]] + runoffVotes[topTwo[1]];
        const runoffResult = Object.keys(runoffVotes).map(candidate => {
            return {
                name: candidate,
                votes: runoffVotes[candidate],
                percentage: ((runoffVotes[candidate] / runoffTotalVotes) * 100).toFixed(2)
            };
        });

        // Sort by runoff vote percentages
        runoffResult.sort((a, b) => b.votes - a.votes);

        result = `${runoffResult[0].name} wins the runoff with ${runoffResult[0].percentage}% of the votes.`;
    }

    // Render the results page and pass the calculated data
    res.render('additional_calculation', { candidates, result });
  } catch (err) {
    console.error('Error calculating election results:', err);
    res.status(500).send('Server Error');
  }
});





router.get('/district-summary/:id', async (req, res) => {
  const districtId = req.params.id;

  try {
    
    const candidates = await Candidates.find({
  districtID: districtId,
  ElectionName: "Parliament"
});


    if (!candidates || candidates.length === 0) {
      return res.status(404).json({ message: "No candidates found for this district." });
    }

   
    const districtSummary = {
      name: districtId,  
      summary: `This is a detailed summary report for ${districtId}.`, 
      candidates: candidates.map(candidate => ({
        name: candidate.Cname,    
        partyname: candidate.partyname,  
        vote_count_option_1:candidate.vote_count_option_1

      }))
    };

    res.json(districtSummary);

  } catch (error) {
    console.error('Error fetching district summary:', error);
    res.status(500).json({ message: 'Error fetching district summary.' });
  }
});


router.post('/deleteparty/:id', async (req, res) => {
  try {
      
      await Party.findByIdAndDelete(req.params.id);
    
      res.redirect('/addparty');
  } catch (error) {
      console.error('Error deleting party:', error);
      res.status(500).send('Server Error');
  }
});

router.post('/deleteCandidate/:id', async (req, res) => {
  try {
    const candidateId = req.params.id;

    await Candidates.findByIdAndDelete(candidateId);

    res.redirect('/addcandidatespl'); 
  } catch (error) {
    console.error('Error deleting candidate:', error.message);
  
    res.redirect('/addcandidatespl'); 
  }
});


router.post('/deletePCandidate/:id', async (req, res) => {
  try {
    const candidateId = req.params.id;


    await Candidates.findByIdAndDelete(candidateId);


    res.redirect('/showCandidates'); 
  } catch (error) {
    console.error('Error deleting candidate:', error.message);
    
    res.redirect('/showCandidates');
  }
});

module.exports = router;