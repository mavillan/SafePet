angular.module('safePet', ['ionic','ngResource','satellizer'])

.config(function ($stateProvider, $urlRouterProvider,$authProvider) {

  // Satellizer config
  $authProvider.loginUrl = "http://safepetapi.labcomp.cl:5000/auth/login";
  $authProvider.signupUrl = "http://safepetapi-labcomp.cl:5000/auth/signup";
  $authProvider.tokenName = "token";
  $authProvider.tokenPrefix = "safepet";


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
            templateUrl: "views/menu/menu.html"
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
});