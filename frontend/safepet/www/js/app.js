angular.module('safePet', ['ionic','ngResource','satellizer','ngImgCrop', 'ngCordova', 'ngFileUpload'])

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
    };

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
    .state('test', {
        url: '/test',
        templateUrl: 'views/test/test.html',
        controller: 'testController'
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
            cache: false,
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
        .state('app.change',{
            url: '/change/:dogId',
            views: {
                'menuContent': {
                    templateUrl: 'views/change/change.html',
                    controller: 'changeController'
                }
            }
        })
        .state('app.newdog',{
            url: '/newdog',
            views: {
                'menuContent':{
                    templateUrl: 'views/newdog/newdog.html',
                    controller: 'newDogController'
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
    return $resource("http://safepetapi.labcomp.cl:5000/users/:id/",{id: "@id"},{update: {method: "PUT"}});
}])

// Given an email, return the users id 
.factory('usersEmailResource', ['$resource', function($resource){
    return $resource("http://safepetapi.labcomp.cl:5000/users/e/:email", {email: "@email"}, {update: {method: "PUT"}});
}])

// Return the dogs resource
.factory('dogsResource', ['$resource', function($resource){
    return $resource("http://safepetapi.labcomp.cl:5000/dogs/:id",{id: "@id"},{update: {method: "PUT"}});
}])

// Return the user dogs resource
.factory('userDogsResource', ['$resource', function($resource){
    return $resource("http://safepetapi.labcomp.cl:5000/dogs/user/:id",{userId: "@id"},{update: {method: "PUT"}});
}])

// Return the lost dogs resource
.factory('lostDogs', ['$resource', function($resource){
    return $resource("http://safepetapi.labcomp.cl:5000/dogs/lost", {}, {});
}])
// Nose imgs storing
.factory('noseImgs', ['$resource', function($resource){
    return $resource("http://safepetapi.labcomp.cl:5000/noseimgs/:id", {id: "@id"}, {});
}])
// Dogs Imgs storing
.factory('dogsImgs', ['$resource', function($resource){
    return $resource("http://safepetapi.labcomp.cl:5000/dogimgs/:id", {id: "@id"}, {});
}])
// Sockect connection 
.factory('socketConn', [function(){
    return io('http://safepetapi.labcomp.cl:5000');
}])

//Camera
.factory('Camera', ['$q', function($q) {
  return {
    getPicture: function(options) {
      var q = $q.defer();
      
      navigator.camera.getPicture(function(result) {
        q.resolve(result);
      }, function(err) {
        q.reject(err);
      }, options);
      
      return q.promise;
    }
  }
}])

// Return current authenticated user
.factory('userInfo', ['$auth', 'usersResource', 'userDogsResource', '$rootScope','socketConn', function($auth,usersResource, userDogsResource, $rootScope, socketConn){
    
    var userInfo = {};

    userInfo.refresh = function(){
        if($auth.isAuthenticated()){
            userInfo.tokenPayload = $auth.getPayload();
            userInfo.userId = userInfo.tokenPayload.sub;
            userInfo.user = usersResource.get({id: userInfo.userId});
            userInfo.dogs = userDogsResource.query({id: userInfo.userId});
            $rootScope.$broadcast('user:refresh', userInfo);
        } else {
            userInfo.user = {};
        }
        
    };

    userInfo.clear = function(){
            userInfo.tokenPayload = null;
            userInfo.userId = null;
            userInfo.user = null;
            userInfo.dogs = null;
    };
    
    return userInfo;
}]);