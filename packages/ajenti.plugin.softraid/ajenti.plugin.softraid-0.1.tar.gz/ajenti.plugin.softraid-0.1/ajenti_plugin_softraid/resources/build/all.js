'use strict';

// the module should depend on 'core' to use the stock services & components
angular.module('ajenti.softraid', ['core']);


'use strict';

angular.module('ajenti.softraid').config(function ($routeProvider) {
    $routeProvider.when('/view/softraid', {
        templateUrl: '/softraid:resources/partial/index.html',
        controller: 'SoftraidIndexController'
    });
});


'use strict';

angular.module('ajenti.softraid').controller('SoftraidIndexController', function ($scope, $http, $interval, pageTitle, gettext, notify) {
    pageTitle.set(gettext('Softraid'));

    $scope.getResources = function () {
        $http.get('/api/softraid').then(function (resp) {
            $scope.raid = resp.data;
            $scope.start_refresh();
        });
    };

    $scope.start_refresh = function () {
        if ($scope.refresh === undefined) $scope.refresh = $interval($scope.getResources, 30000, 0);
    };

    $scope.getResources();

    $scope.$on('$destroy', function () {
        return $interval.cancel($scope.refresh);
    });
});


