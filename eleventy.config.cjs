module.exports = function(eleventyConfig){
  eleventyConfig.setUseGitIgnore(false); // process src/ even if .gitignore ignores it
  
  // Pass through CSS and other assets
  eleventyConfig.addPassthroughCopy("src/assets");
  
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