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
	.state('app.profile', {
 	    url: '/profile',
	    views: {
		'menuContent': {
		    templateUrl: 'views/profile/profile.html',
		    controller: 'profileController'
		}
	   }
	})
	.state('app.editProfile', {
 	    url: '/edit',
	    views: {
		'menuContent': {
		    templateUrl: 'views/editProfile/editProfile.html',
		    controller: 'editController'
		}
	   }
	})
        .state('app.notifications',{
            url: '/notifications',
            views: {
                'menuContent': {
                    templateUrl: 'views/notifications/notifications.html',
                    controller: 'notificationsController'
                }
            }
        })
        .state('app.faq',{
            url: '/faq',
            views: {
                'menuContent': {
                    templateUrl: 'views/faq/faq.html',
                }
            }
        })
        .state('app.settings',{
            url: '/settings',
            views: {
                'menuContent': {
                    templateUrl: 'views/settings/settings.html',
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
    if($auth.isAuthenticated()){
        var tokenPayload = $auth.getPayload();
        var userId = tokenPayload.sub;
    }
    return usersResource.get({id: userId});
}]);
