
var app = angular.module('MainApp',[]);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.run();app.controller('IdsGeneratorCtrl', ['$scope', '$http', '$window', function($scope, $http, $window) {
    $scope.nonPatentRows = [{}];
    $scope.usPatentRows = [{}];
    $scope.usApplicationRows = [{}];
    $scope.foreignApplicationRows = [{}];
    $scope.itemCited = 1;
    $scope.signature_changed = false;

    $scope.signature_changed = function() {
        $scope.signature_changed = true
    }

    $scope.signature_name_changed = function() {
        console.debug('gseg')
        $scope.signature = "/" + $scope.signature_name + "/"
    }

    $scope.addNonPatentRow = function (rows_to_add){
        for(i = 0; i < rows_to_add; i++) {
            $scope.nonPatentRows.push({});
        }
    }

    $scope.addUsPatentRow = function (rows_to_add){
        for(i = 0; i < rows_to_add; i++) {
            $scope.usPatentRows.push({});
        }
    }

    $scope.addUsApplicationRow = function (rows_to_add){
        for (i = 0; i < rows_to_add; i++) {
            $scope.usApplicationRows.push({});
        }
    };

    $scope.addForeignApplicationRow = function (rows_to_add){
        for(i = 0; i < rows_to_add; i++) {
            $scope.foreignApplicationRows.push({});
        }
    };

        $scope.updateAllCitedSelection = function (){
            if($scope.each_item_cited)
        {
            $scope.no_item_cited = false;
        }
    };

    $scope.updateNoCitedSelection = function (){
        if($scope.no_item_cited)
        {
            $scope.each_item_cited = false;
        }
    };

    $scope.fillInApplicationData = function (application){
        $scope.loading_application_data = true;
        $scope.loading_message = "loading application data.."

        $http.get('/idsgenerator/applicationdata', {
            params: {
                application_number: $scope.application
            }
        }).
            success(function(data, status, headers, config) {
                console.debug(data);
                $scope.filing_date = data['filing_date'];
                $scope.first_named_inventor = data['first_named_inventor'];
                $scope.art_unit = data['art_unit'];
                $scope.examiner_name = data['examiner_name'];
                $scope.attorney_docket_number = data['attorney_docket_number'];

                $scope.loading_application_data = false;
                $scope.loading_message = ""
        }).
            error(function(data, status, headers, config) {
                $scope.loading_application_data = false;
                $scope.loading_message = "Cannot Get Data. Please fill in manually."
        })};

    $scope.fillInUsPatentData = function (usPatent){
        $http.get('/idsgenerator/uspatentdata', {
            params: {
                us_patent: usPatent.number
            }
        }).then(function (response) {
                var data = response['data'];
                console.debug(data);
                usPatent.date = data['date'];
                usPatent.inventor = data['inventor'];
        });
    };

    $scope.fillInUsApplicationData = function (usApplication){
            $http.get('/idsgenerator/usapplicationdata', {
                params: {
                    us_application: usApplication.number
                }
            }).then(function (response) {
                    var data = response['data'];
                    console.debug(data);
                    usApplication.date = data['date'];
                    usApplication.inventor = data['inventor'];
            });
        };

    $scope.fillInForeignApplicationData = function (foreignApplication){
            $http.get('/idsgenerator/foreignapplicationdata', {
                params: {
                    foreign_application: foreignApplication.number
                }
            }).then(function (response) {
                    var data = response['data']
                    console.debug(data);
                    foreignApplication.date = data['date'];
                    foreignApplication.inventor = data['inventor'];
            });
        }

    $scope.submit = function (){
        $http.post('/idsgenerator/generate',
            {
                application_number: $scope.application,
                filing_date: $scope.filing_date,
                first_named_inventor: $scope.first_named_inventor,
                art_unit: $scope.art_unit,
                examiner_name: $scope.examiner_name,
                attorney_docket_number: $scope.attorney_docket_number,
                us_patents: $scope.usPatentRows,
                us_applications: $scope.usApplicationRows,
                foreign_applications: $scope.foreignApplicationRows,
                non_patent_literature: $scope.nonPatentRows,
                each_item_cited: $scope.each_item_cited,
                no_item_cited: $scope.no_item_cited,
                certification_attached: $scope.certification_attached,
                fee_submitted: $scope.fee_submitted,
                certification_not_submitted: $scope.certification_not_submitted,
                signature_name: $scope.signature_name,
                signature_registration_number: $scope.signature_registration_number
            }
        ).
        success(function(data, status, headers, config) {
                file_url = data['url']
                $window.open(file_url)
            // this callback will be called asynchronously
            // when the response is available
          }).
        error(function(data, status, headers, config) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
          });
    }
}]);