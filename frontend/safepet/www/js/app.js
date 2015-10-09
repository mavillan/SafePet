angular.module('safePet', ['ionic','ngResource','satellizer'])

.config(function ($stateProvider, $urlRouterProvider,$authProvider) {

    // Satellizer config
    $authProvider.baseUrl = 'http://safepetapi.labcomp.cl:5000';
    $authProvider.loginUrl = "/auth/login";
    $authProvider.signupUrl = "/auth/signup";
    $authProvider.tokenName = "token";
    $authProvider.tokenPrefix = "safepet";

    var facebookCfg = {
        popupOptions: {
            location: 'no',
            toolbar: 'no',
            width: window.screen.width,
            height: window.screen.height
        },
        url: '/auth/facebook',
        clientId: '1460728627588325',
    };

    var twitterCfg = {
        popupOptions: {
            location: 'no',
            toolbar: 'no',
            width: window.screen.width,
            height: window.screen.height
        },
        url: '/auth/twitter'
    }

    if (ionic.Platform.isIOS() || ionic.Platform.isAndroid()) {
        $authProvider.platform   = 'mobile';
        facebookCfg.redirectUri  = 'http://127.0.0.1/';
        twitterCfg.redirectUri   = 'http://127.0.0.1/';
    } else {
        $authProvider.withCredentials = false;
    }

    // Facebook Login
    $authProvider.facebook(facebookCfg);

    // Twitter Login
    $authProvider.twitter(twitterCfg);


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
        })
        .state('app.notifications',{
            url: '/notifications',
            views: {
                'menuContent': {
                    templateUrl: 'views/notifications/notifications.html',
                    controller: 'notificationsController'
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

    var userInfo = {};

    userInfo.refresh = function(){
        if($auth.isAuthenticated()){
            userInfo.tokenPayload = $auth.getPayload();
            userInfo.userId = userInfo.tokenPayload.sub;
            userInfo.user = usersResource.get({id: userInfo.userId});
        }
        
    };

    userInfo.clear = function(){
            userInfo.tokenPayload = null;
            userInfo.userId = null;
            userInfo.user = null;
    };
    return userInfo;
}]);