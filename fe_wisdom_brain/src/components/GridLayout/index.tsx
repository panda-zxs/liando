import React from 'react';
import ReactGridLayout from 'react-grid-layout';

import './style.less';

interface IGridLayoutProps extends ReactGridLayout.ReactGridLayoutProps {}

export default class GridLayout extends React.Component<IGridLayoutProps> {
  public render() {
    const { children, layout, ...otherProps } = this.props;
    return (
      <div>
        <ReactGridLayout
          className="layout"
          layout={layout}
          cols={12}
          rowHeight={40}
          width={1200}
          {...otherProps}
        >
          {React.Children.map(children, Child => Child)}
        </ReactGridLayout>
      </div>
    );
  }
}
