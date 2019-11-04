// db.database.dropIndex();
// for(var i=0;i<10;i++)
// {
//   console.log(Math.ceil(Math.random()*6));
// }
var express = require("express"),
    app     = express(),
    mongoose = require("mongoose"),
    bodyParser = require("body-parser"),
    passport  = require("passport"),
    expressSession = require("express-session"),
    localstratergy = require("passport-local");

//-------------------Routes-----------------------------------------------
var indexroutes = require("./routes/index.js");
    // shopUser = require("./routes/shopUser.js"),
    // shopCustomer = require("./routes/shopCustomer.js");
//--------------------------------------------------------------
//var medicine = require("./models/item.js")
    user     = require("./models/user.js");
    // collectedpage = require("./models/collectedpage.js");
    link = require("./models/link.js");

    // collectedpage.find({},function(err,foundcollectedpages){
    //   if(err){ console.log(err);}
    //   else {
    //     // res.render("index/index.ejs",{user: foundusers, pages: foundcollectedpages});
    //     console.log(foundcollectedpages)
    //   }
    // });

    link.find({},function(err,foundlinks){
      if(err){ console.log(err);}
      else {
        // res.render("index/index.ejs",{user: foundusers, pages: foundcollectedpages});
        // console.log(foundlinks)
      }
    });

  
//--------------------------------------------------------------
// mongoose.connect("mongodb://nachijr4:PAssword00!!@ds113871.mlab.com:13871/medsys",{useNewUrlParser: true});
// mongoose.connect(process.env.database,{useNewUrlParser: true});
mongoose.connect("mongodb://localhost:27017/TheBlink",{useNewUrlParser: true});
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
// app.use(shopUser);
// app.use(shopCustomer);
app.listen(3000, function(){
  console.log("Server Started")
});
