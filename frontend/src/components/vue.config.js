const fs = require("fs");

module.exports = {
  devServer: {
    https: {
      key: fs.readFileSync("./key.pem"),
      cert: fs.readFileSync("./cert.pem"),
    },
    port: 5173,
  },
};
