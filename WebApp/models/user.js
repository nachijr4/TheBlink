var mongoose = require("mongoose");
      plm     = require("passport-local-mongoose");


userSchema =new mongoose.Schema({
  name: String,
  username: String,
  password: String,
  isAdmin: Boolean
});

userSchema.plugin(plm);

module.exports = mongoose.model("user",userSchema);
