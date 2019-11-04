var mongoose = require("mongoose");


linkSchema =new mongoose.Schema({
    url : String,
    title : String,
    thumbnail : String,
    description : String,
    html : String,
    content_category : String,
    page_classes_prob : Object,
    summary : String,
    created_at: Date,
    updated_at: Date
});


module.exports = mongoose.model("link",linkSchema);