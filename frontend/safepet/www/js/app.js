angular.module('safePet', ['ionic','ngResource'])

.config(function ($stateProvider, $urlRouterProvider) {

  $stateProvider
    .state('mainList', {
      url: '/',
      controller: 'mainListController',
      templateUrl: 'views/mainList/mainList.html'
    });

  $urlRouterProvider.otherwise('/');

});
