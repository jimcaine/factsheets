import React from 'react'

class Header extends React.Component {
  constructor() {
    super()
  }

  render() {
    return (
      <div>
        <h1>Fund name: <span id="fund_name">{this.props.fundName}</span></h1>
      </div>
    )
  }
}

export default Header