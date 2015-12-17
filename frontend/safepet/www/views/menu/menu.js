angular.module('safePet')


.controller('menuController', ['$scope','$auth','$state','userInfo','$ionicHistory','$timeout','$ionicPopup' , 'userDogsResource', function($scope,$auth,$state,userInfo,$ionicHistory,$timeout,$ionicPopup, userDogsResource){

	// Refresh user information
	userInfo.refresh();

	if($auth.isAuthenticated()){
	// Handle user information from the API
	userInfo.user.$promise.then(function(user){
		userInfo.refresh();
		$scope.menuTitle = user.displayName;
		$scope.dogs = userDogsResource.query({id: user._id});
	});
	
	}
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

    $scope.showAlert = function() {
   		var alertPopup = $ionicPopup.alert({
     			title: 'Acerca de SafePet',
     			template: 'SafePet es un producto de OverPi pensado en la seguridad de tu perro. Si desea obtener mayor información puede dirigirse a nuestra <a href="http://overpi.feriadesoftware.cl/">Página web</a> o nuestro <a href="https://www.facebook.com/safepet.cl?fref=ts">Facebook.</a>' 
   		});
 	};
	
}]);
