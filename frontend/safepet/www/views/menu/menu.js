angular.module('safePet')


.controller('menuController', ['$scope','$auth','$state','userInfo','$ionicHistory','$timeout','$ionicPopup' , 'userDogsResource', '$interval', 'socketConn', function($scope,$auth,$state,userInfo,$ionicHistory,$timeout,$ionicPopup, userDogsResource, $interval,socketConn){

	// Refresh user information
	userInfo.refresh();
	// Event listener: update dog count
	/*userInfo.user.$promise.then(function(user){
		$scope.menuTitle = user.displayName;
	});*/
	// This one is necessary since menuController only charges one time.	
	$scope.$on('user:refresh', function(event, data){
		// Handle user information from the API
		userInfo.user.$promise.then(function(user){
			$scope.menuTitle = user.displayName;
		});
		$scope.dogs = data.dogs;
	});

	$scope.logout = function(){
		$auth.logout()
		.then(function() {
			userInfo.clear();
			//Example of socket 
			socketConn.emit('logout', { userId: userInfo.userId });
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
     			template: 'SafePet es un producto de OverPi pensado en la seguridad de tu perro. Si desea obtener mayor información puede dirigirse a nuestra <a href="http://safepet.feriadesoftware.cl/">Página web</a> o nuestro <a href="https://www.facebook.com/safepet.cl?fref=ts">Facebook.</a>' 
   		});
 	};
}]);
