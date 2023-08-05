/* eslint-env node */

"use strict";

const gulp = require("gulp");

const autoprefixer = require("autoprefixer");
const json_importer = require("node-sass-json-importer");
const plumber = require("gulp-plumber");
const postcss = require("gulp-postcss");
const postcss_scss = require("postcss-scss");
const rename = require("gulp-rename");
const reporter = require("postcss-reporter");
const sass = require("gulp-sass");
const sourcemaps = require("gulp-sourcemaps");
const stylelint = require("stylelint");

sass.compiler = require("node-sass");

// #############################################################################
// SASS

gulp.task("sass", () => {
  return gulp.src("x_net_django_email_template/static_src/scss/**/*.scss")
    .pipe(plumber())
    .pipe(sourcemaps.init())
    .pipe(postcss([
      stylelint(),
      reporter({
        clearReportedMessages: true,
      }),
    ], {
      syntax: postcss_scss,
    }))
    .pipe(
      sass.sync({
        outputStyle: "compressed",
        importer: json_importer(),
        // importer: json_importer({
        //   resolver: function(dir, url) {
        //     // console.log(dir, url)
        //     return url.startsWith('~/') ? path.resolve(dir, 'json', url.substr(2)) : path.resolve(dir, url);
        //   },
        // }),
      }).on("error", sass.logError)
    )
    .pipe(rename({
      suffix: ".min",
    }))
    .pipe(postcss([
      autoprefixer(),
    ]))
    .pipe(sourcemaps.write("."))
    .pipe(gulp.dest("x_net_django_email_template/static/css/"));
});

// #############################################################################
// TASK

exports.default = function () {
  gulp.watch("x_net_django_email_template/static_src/scss/**/*.scss", gulp.series("sass"));
};
