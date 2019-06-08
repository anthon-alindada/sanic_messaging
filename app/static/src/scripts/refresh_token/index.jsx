// Core
import Cookies from 'js-cookie'
import moment from 'moment'
import axios from 'axios'


const refreshToken = () => {
  const jwtExpiration = Cookies.get('jwt_expiration')

  // If not existing logout auto
  if (jwtExpiration === undefined) {
    window.location = '/logout'
  }

  // Check if expired
  // And reload
  if (jwtExpiration < moment().unix()) {
    const axiosInstance = axios.create({
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'x-csrf-token': Cookies.get('csrf_token'),
      },
    })
    axiosInstance.post('/refresh_token')
  }
}


setInterval(refreshToken, 1000)
