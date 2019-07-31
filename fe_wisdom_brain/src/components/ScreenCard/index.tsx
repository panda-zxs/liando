import React from 'react';
import styles from './style.less';

interface IScreenCardProps {
  className?: string;
}

export default class ScreenCard extends React.PureComponent<IScreenCardProps> {
  public render() {
    const { className, ...otherProps } = this.props;
    return (
      <div className={`${styles.card} ${className}`} {...otherProps}>
        {this.props.children}
      </div>
    );
  }
}
