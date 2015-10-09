angular.module('safePet')

.controller('menuController', ['$scope','$auth','$state','userInfo', '$ionicPopup', function($scope,$auth,$state, userInfo, $ionicPopup){
	userInfo.$promise.then(function(user){
		$scope.menuTitle = user.displayName;
	});
	
	$scope.logout = function(){
		$auth.logout()
		.then(function() {
            $state.go("login");
        });
	};

        $scope.showAlert = function() {
   		var alertPopup = $ionicPopup.alert({
     			title: 'Acerca de SafePet',
     			template: 'SafePet es un producto de OverPi pensado en la seguridad de tu perro. Si desea obtener mayor información puede dirigirse a nuestra <a href="http://overpi.feriadesoftware.cl/">Página web</a> o nuestro <a href="https://www.facebook.com/safepet.cl?fref=ts">Facebook.</a>' 
   		});
 	};
	
}]);
