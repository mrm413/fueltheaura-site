module.exports = function(eleventyConfig){
  eleventyConfig.setUseGitIgnore(false); // process src/ even if .gitignore ignores it
  return { dir:{ input:"src", output:"dist", includes:"layouts", data:"_data" } };
};
