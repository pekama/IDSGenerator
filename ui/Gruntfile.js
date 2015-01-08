module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    watch: {
      js: {
        options: {
          livereload: true,
            spawn: false
        },
        files: [
          'src/js/**/*.js',
          'src/js/**/**/*.js',
          'Gruntfile.js',
          'bower.json'
        ],
        tasks: ['jshint', 'concat']
      },

      templates: {
        options: {
          livereload: true,
            spawn: false
        },
        files: [
          'src/js/templates/**.html',
          'src/js/templates/**/**.html'
        ],
        tasks: ['ngtemplates']
      }
    },

    jshint: {
      options: {
        force: true,
        asi: true
      },
      all: ['Gruntfile.js', 'src/js/**/*.js', 'src/js/**/**/*.js']
    },

    concat: {
      options: {
        nonull: true,
        separator: ';'
      },
      vendors: {
        src: [
          './bower_components/jquery/dist/jquery.js',
          './bower_components/bootstrap/dist/js/bootstrap.js',
          './bower_components/bootstrap-select/js/bootstrap-select.js',
          './bower_components/angular/angular.js',
          './bower_components/angular-cookies/angular-cookies.js',
          './bower_components/angular-resource/angular-resource.js',
          './bower_components/angular-bootstrap/ui-bootstrap.js',
          './bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
        ],
        dest: '../idsgenerator/static/js/vendors.js'
      },

      application: {
        src: [
          './src/js/app.js',
          './src/js/**/controllers/*.js',
        ],
        dest: '../idsgenerator/static/js/application.js'
      },
    },

    uglify: {
      vendors: {
        options: {
          sourceMap: false
        },
        files: {
          'public/js/vendors.min.js': ['public/js/vendors.js']
        }
      },
      application: {
        options: {
          sourceMap: false
        },
        files: {
          'public/js/application.min.js': ['public/js/application.js', 'public/js/templates.js']
        }
      }
    },

    ngtemplates:  {
      MainApp:        {
        src:      ['src/js/templates/**.html', 'src/js/templates/**/**.html'],
        dest:     '../idsgenerator/static/js/templates.js'
      }
    },
  });

  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-symlink');
  grunt.loadNpmTasks('grunt-angular-templates');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-clean');


  // Default task(s).
  grunt.registerTask('build', ['ngtemplates', 'concat']);
  grunt.registerTask('default', ['build', 'watch']);
};

