var express = require("express"),
    app     = express(),
    mongoose = require("mongoose"),
    bodyParser = require("body-parser"),
    passport  = require("passport"),
    expressSession = require("express-session"),
    localstratergy = require("passport-local");

//-------------------Routes-----------------------------------------------
var indexroutes = require("./routes/index.js");
//--------------------------------------------------------------
    user     = require("./models/user.js");
    link = require("./models/link.js");
//--------------------------------------------------------------
mongoose.connect("mongodb://localhost:27017/TheBlink",{useNewUrlParser: true, useUnifiedTopology: true});
mongoose.set('useCreateIndex', true);
console.log(__dirname);
app.use(express.static(__dirname +"/public"));
app.use(bodyParser.urlencoded({extended: true}));
//--------------------------------------------------------------

passport.use(new localstratergy(user.authenticate()));
app.use(expressSession({
  secret:"secret of the med system",
  resave: false,
  saveUninitialized: false
}));
app.use(passport.initialize());
app.use(passport.session());
passport.serializeUser(user.serializeUser());
passport.deserializeUser(user.deserializeUser());

//--------------------------------------------------------------


app.use(function(req,res,next){
  res.locals.currentUser = req.user;
  next();
});

app.use(indexroutes);
app.listen(3000, function(){
  console.log("Server Started")
});
