module.exports = {
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
      builderOptions: {
        files: [
          "**/*",
          {
            from: "./*",
            to: "./*",
            filter: [ "**/*" ]
          }
        ],
        extraFiles: [
          {
            from: "./lib",
            to: "./",
            filter: [ "**/*" ]
          }
        ]
      }
    }
  }
}