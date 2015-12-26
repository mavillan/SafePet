angular.module('safePet')


.controller('menuController', ['$scope','$auth','$state','userInfo','$ionicHistory','$timeout','$ionicPopup' , 'userDogsResource', '$interval', function($scope,$auth,$state,userInfo,$ionicHistory,$timeout,$ionicPopup, userDogsResource, $interval){

	// Refresh user information
	userInfo.refresh();
	// Handle user information from the API
	userInfo.user.$promise.then(function(user){
		$scope.menuTitle = user.displayName;
		$scope.dogs = userDogsResource.query({id: user._id});
	});
	
	$scope.logout = function(){
		$auth.logout()
		.then(function() {
			userInfo.clear();
            $state.go("login");
    		$timeout(function () {
        		$ionicHistory.clearCache();
        		$ionicHistory.clearHistory();
    		}, 1500)
        });
	};

	$interval(function(){
		userInfo.user.$promise.then(function(user){
			$scope.menuTitle = user.displayName;
			$scope.dogs = userDogsResource.query({id: user._id});
		});
	}, 5000)

    $scope.showAlert = function() {
   		var alertPopup = $ionicPopup.alert({
     			title: 'Acerca de SafePet',
     			template: 'SafePet es un producto de OverPi pensado en la seguridad de tu perro. Si desea obtener mayor información puede dirigirse a nuestra <a href="http://overpi.feriadesoftware.cl/">Página web</a> o nuestro <a href="https://www.facebook.com/safepet.cl?fref=ts">Facebook.</a>' 
   		});
 	};
	
}]);
