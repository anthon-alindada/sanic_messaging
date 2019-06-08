const path = require('path');


/**
 * Webpack configs
 */
module.exports = {
  context: path.join(__dirname, 'src/scripts'),
  cache: true,
  entry: {
    signup: './signup/index.jsx',
    login: './login/index.jsx',
    refresh_token: './refresh_token/index.jsx',
  },
  output: {
    path: path.join(__dirname, 'dist', 'scripts'),
    filename: '[name].min.js',
  },
  module: {
    rules: [
      {
        test: /\.jsx$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
        },
      },
      {
        test: /\.scss$/,
        use: [
          {
            loader: 'style-loader',
          },
          {
            loader: 'css-loader',
          },
          {
            loader: 'sass-loader',
          },
        ],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
    alias: {
      core: path.resolve('./src/scripts/core'),
    },
  },
  devtool: 'source-map',
};
