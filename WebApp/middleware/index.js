var middlewareObj = {};

middlewareObj.isLoggedIn = function(req,res,next){
  if(req.isAuthenticated()){
    return next();
  }
  else{
    res.redirect("/login");
  }
}

middlewareObj.isAdmin = function(req,res,next){
  if(req.user.isAdmin === true){
    return next();
  }
  else{
    res.redirect("/home");
  }
}

middlewareObj.isCustomer = function(req,res,next){
  if(req.user.isAdmin === false){
    return next();
  }
  else{
    res.redirect("/"+req.user.username);
  }
}

middlewareObj.isNotLoggedIn = function(req,res,next){
  if(!req.isAuthenticated()){
    return next();
  }
  else{
    res.redirect("/home");
  }
}


module.exports = middlewareObj;
