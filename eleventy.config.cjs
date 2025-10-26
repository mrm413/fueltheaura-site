const markdownIt = require("markdown-it");

module.exports = function(eleventyConfig){
  eleventyConfig.setUseGitIgnore(false); // process src/ even if .gitignore ignores it
  
  // Configure markdown processing
  const md = markdownIt({
    html: true,
    breaks: true,
    linkify: true
  });
  
  // Add markdown filter for processing markdown in templates
  eleventyConfig.addFilter("markdown", function(content) {
    return md.render(content);
  });
  
  // Set markdown library
  eleventyConfig.setLibrary("md", md);
  
  // Pass through CSS and other assets
  eleventyConfig.addPassthroughCopy("src/assets");
  
  // Add blog posts collection
  eleventyConfig.addCollection("blogPosts", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/blog/posts/*.njk").reverse();
  });
  
  // Add date filter for formatting dates
  eleventyConfig.addFilter("date", function(date, format) {
    const d = new Date(date);
    const months = ["January", "February", "March", "April", "May", "June", 
                    "July", "August", "September", "October", "November", "December"];
    return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
  });
  
  // Add truncate filter for excerpts
  eleventyConfig.addFilter("truncate", function(text, length) {
    if (!text) return "";
    const stripped = text.replace(/<[^>]+>/g, '').replace(/\n/g, ' ');
    if (stripped.length <= length) return stripped;
    return stripped.substr(0, length) + '...';
  });
  
  // Add limit filter for limiting array items
  eleventyConfig.addFilter("limit", function(array, limit) {
    if (!Array.isArray(array)) return array;
    return array.slice(0, limit);
  });
  
  return { 
    dir:{ 
      input:"src", 
      output:"dist", 
      includes:"_includes",
      layouts:"_includes",
      data:"_data" 
    } 
  };
};