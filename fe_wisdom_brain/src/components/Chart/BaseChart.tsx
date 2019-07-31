import React from 'react';
import * as echarts from 'echarts';
import elementResizeEvent from 'element-resize-event';

interface IBaseChart {
  height?: string | number;
  isLazy?: boolean;
  style?: React.CSSProperties;
}

interface IChartEvents {
  [eventName: string]: (param?: any) => any;
}

export default class BaseChart extends React.Component<IBaseChart> {
  public chartDom: HTMLDivElement = null;

  public myChart: echarts.ECharts = null;

  public static defaultProps: IBaseChart = {
    height: '100%',
  };

  public chartEvents?: IChartEvents;

  public onChartDomClick = (event: React.SyntheticEvent) => {};

  public componentDidMount() {
    console.log('renderChart did');
    this._initChart();
  }

  public getOption(props = this.props): echarts.EChartOption {
    return null;
  }

  private _initChart() {
    console.log('renderChart initChart');
    const { isLazy } = this.props;
    this.getOption();
    if (this.chartDom) {
      if (!isLazy) {
        const option = this.getOption();
        this.myChart = echarts.init(this.chartDom);
        this.myChart.setOption(option);
        elementResizeEvent(this.chartDom, () => {
          console.log('update');
          this.myChart.resize();
        });
        this._initChartEvents();
      }
    }
  }

  private _initChartEvents = () => {
    Object.keys(this.chartEvents).forEach(eventName => {
      console.log(eventName);
      this.myChart.on(eventName, this.chartEvents[eventName]);
    });
  };

  public render() {
    console.log('renderChart render');
    const { height, style } = this.props;
    // return null
    return (
      <div
        onClick={this.onChartDomClick}
        ref={dom => (this.chartDom = dom)}
        style={{ ...style, height }}
      />
    );
  }
}
