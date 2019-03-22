'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var merge = require('merge-stream');

var sass_conf = {
    errLogToConsole: true,
    outputStyle: 'compressed'
};

var sass_folders = [
    {
        'src': 'minimalist_cms/cms_toolbar/static/cms_toolbar/sass/**.sass',
        'dest': 'minimalist_cms/cms_toolbar/static/cms_toolbar/css/',
    },
];

var do_sass = function(src_path, dest_path) {
    return gulp.src(src_path)
        .pipe(sass(sass_conf).on('error', sass.logError))
        .pipe(gulp.dest(dest_path));
}


gulp.task('sass', function () {
    var streams = [];
    for (var i=0; i<sass_folders.length; i++) {
        streams.push(do_sass(sass_folders[i].src, sass_folders[i].dest));
    }
    return merge(streams);
});


gulp.task('watch', function () {
    gulp.watch('minimalist_cms/**/*.sass', gulp.parallel('sass'));
});
