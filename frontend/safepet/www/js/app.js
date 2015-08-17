angular.module('safePet', ['ionic','ngResource','satellizer'])

.config(function ($stateProvider, $urlRouterProvider,$authProvider) {

    // Satellizer config
    $authProvider.loginUrl = "http://safepetapi.labcomp.cl:5000/auth/login";
    $authProvider.signupUrl = "http://safepetapi.labcomp.cl:5000/auth/signup";
    $authProvider.tokenName = "token";
    $authProvider.tokenPrefix = "safepet";
    $authProvider.platform = 'mobile';

    // Router Config
    $stateProvider
        .state('login', {
            url: '/login',
            templateUrl: 'views/auth/login.html',
            controller: 'authController'
        })
        .state('app', {
            url: "/app",
            abstract: true,
            templateUrl: "views/menu/menu.html",
            controller: 'menuController'
        })
        .state('app.mainList', {
            url: '/mainlist',
            views: {
                'menuContent': {
                    templateUrl: 'views/mainList/mainList.html',
                    controller: 'mainListController'
                }
            }
        })
        .state('app.dogDetails', {
            url: '/:dogId',
            views: {
                'menuContent': {
                    templateUrl: 'views/dogDetails/dogDetails.html',
                    controller: 'dogDetailsController'
                }
            }
        });

    $urlRouterProvider.otherwise('/app/mainlist');
})


// Return the users resource
.factory('usersResource', ['$resource', function($resource){
    return $resource("http://safepetapi.labcomp.cl:5000/users/:id",{id: "@id"},{update: {method: "PUT"}});
}])

// Return the dogs resource
.factory('dogsResource', ['$resource', function($resource){
    return $resource("http://safepetapi.labcomp.cl:5000/dogs/:id",{id: "@id"},{update: {method: "PUT"}});
}])

// Return the user dogs resource
.factory('userDogsResource', ['$resource', function($resource){
    return $resource("http://safepetapi.labcomp.cl:5000/dogs/user/:id",{userId: "@id"},{update: {method: "PUT"}});
}])

// Return current authenticated user
.factory('userInfo', ['$auth', 'usersResource', function($auth,usersResource){
    var tokenPayload = $auth.getPayload();
    var userId = tokenPayload.sub;

    return usersResource.get({id: userId});
}]);