var gulp = require('gulp');
//var browserSync = require('browser-sync').browserSync;
var changed = require('gulp-changed');
var exec = require('child_process').exec;
var gutil = require('gulp-util');
//var flatten = require('gulp-flatten');
var runSequence = require('run-sequence');

gulp.task('static', function() {
  return gulp.src('static/**')
    .on('error', function (err) {
      console.log(err);
      gutil.beep();
      this.end();
    })
    .pipe(gulp.dest('site/static'));
});

gulp.task('slides', function() {
  return gulp.src('slides/**')
    .on('error', function (err) {
      console.log(err);
      gutil.beep();
      this.end();
    })
    .pipe(gulp.dest('site/static/slides'));
});

gulp.task('templates', function() {
  exec('./env/bin/python compile.py', function(err, stdout, stderr) {
    console.log(stdout);
    if(err || stderr) {
      console.log(stderr);
      console.log(err);
      gutil.beep();
    }
  });
});

gulp.task('build', function() {
  return runSequence('templates');
});

gulp.task('watch', function() {
  gulp.watch('*.py', ['templates']);
  gulp.watch('templates/**/*.html', ['templates']);
  gulp.watch('static/**/*.{js,jpg,jpeg,png}', ['static']);
  gulp.watch('slides/**/*.{js,jpg,jpeg,png}', ['slides']);
  gulp.watch('static/**/*.css', ['static']);
});
