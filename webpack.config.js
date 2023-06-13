const path = require("path");
const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
  mode: "production",
  entry: "./sphinxcontrib/cadquery/static/index.js",
  output: {
    path: path.resolve(__dirname, "sphinxcontrib/cadquery/static/dist"),
    filename: "vtk-custom.js",
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        {
          from: "*.js",
          context: path.resolve(__dirname, "node_modules", "vtk.js"),
          to: path.resolve(__dirname, "sphinxcontrib/cadquery/static/dist"),
        },
      ],
    }),
  ],
};
