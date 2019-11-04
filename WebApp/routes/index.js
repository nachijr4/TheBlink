var express = require("express"),
    app = express(),
    routes  = express.Router(),
    passport = require("passport"),
    middleware = require("../middleware/index.js"),
    users = require("../models/user.js");
    links = require("../models/link.js");
    // collectedPages = require("../models/collectedPage.js");
    // links.find({},function(err,foundlinks){
    //   console.log(foundlinks)
    // });
    

routes.get("/",middleware.isNotLoggedIn,function(req,res){
  res.render("index/landing.ejs");
})


routes.get("/home",middleware.isLoggedIn,middleware.isCustomer,function(req,res){
  users.find({},function(err,foundusers){
    if(err){ console.log(err);}
    else {
      links.find({},function(err,foundlinks){
        if(err){ console.log(err);}
        else {
          res.render("index/index.ejs",{user: foundusers, pages: foundlinks});
          // console.log(foundlinks)
        }
      });
      //console.log(req.user);
    }
  });
});

//-----------------------------------Adding Users------------------------
// routes.get("/adduser", function(req,res){
//   res.render("index/adduser.ejs");
// });

// routes.post("/adduser",function(req,res){
//   var username = new user({username: req.body.username});
//   users.register(username,req.body.password,function(err, newUser){
//     if(err){console.log(err);}
//     else{
//       newUser.location = req.body.location;
//       newUser.image = req.body.image;
//       newUser.isAdmin = true;
//       newUser.save();
//       var authenticate = passport.authenticate("local");
//       authenticate(req,res,function(){
//         res.redirect("/"+newUser.username);
//       });
//     }
//   });
// });

routes.get("/addcustomer", function(req,res){
  res.render("index/addcustomer.ejs");
});

routes.post("/addcustomer",function(req,res){
  var username = new user({username: req.body.username});
  users.register(username,req.body.password,function(err, newUser){
    if(err){console.log(err);}
    else{
      newUser.name = req.body.name;
      newUser.isAdmin = false;
      newUser.save();
      var authenticate = passport.authenticate("local");
      authenticate(req,res,function(){
        res.redirect("/home");
      });
    }
  });
});
//-----------------------------------------------------------------------
routes.get("/login", function(req, res){
  res.render("index/login.ejs");
});

routes.post("/login",passport.authenticate("local",{successRedirect: "/home",failureRedirect: "/login"}),function(req,res){});

routes.get("/logout",function(req,res){
  req.logout();
  res.redirect("/");
})

module.exports = routes;
